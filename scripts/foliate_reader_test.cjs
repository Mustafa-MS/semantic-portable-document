/* Independent EPUB reader trial using the upstream Foliate JS demo reader. */
const fs = require("fs");
const http = require("http");
const path = require("path");
const { chromium } = require("playwright");

async function main() {
  const [rootArg, outputArg, screenshotsArg, chromeArg, ...epubArgs] = process.argv.slice(2);
  if (!rootArg || !outputArg || !screenshotsArg || !chromeArg || !epubArgs.length) throw new Error("missing arguments");
  const root = path.resolve(rootArg), output = path.resolve(outputArg), screenshots = path.resolve(screenshotsArg);
  fs.mkdirSync(path.dirname(output), { recursive: true }); fs.mkdirSync(screenshots, { recursive: true });
  const types = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".svg": "image/svg+xml" };
  const server = http.createServer((request, response) => {
    const pathname = decodeURIComponent(new URL(request.url, "http://127.0.0.1").pathname).replace(/^\/+/, "");
    if (pathname === "favicon.ico") { response.writeHead(204); response.end(); return; }
    const target = path.resolve(root, pathname);
    if (!target.startsWith(root) || !fs.existsSync(target) || !fs.statSync(target).isFile()) { response.writeHead(404); response.end(); return; }
    response.writeHead(200, { "Content-Type": types[path.extname(target)] || "application/octet-stream" });
    fs.createReadStream(target).pipe(response);
  });
  await new Promise(resolve => server.listen(0, "127.0.0.1", resolve));
  const port = server.address().port;
  const browser = await chromium.launch({ executablePath: path.resolve(chromeArg), headless: true });
  const representative = new Set(["T01", "T04", "T05", "T08", "T09"]), results = [];
  try {
    for (const epubArg of epubArgs) {
      const testId = path.basename(epubArg, ".epub");
      const page = await browser.newPage({ viewport: { width: 1100, height: 780 }, deviceScaleFactor: 1 });
      const consoleErrors = []; page.on("console", message => { if (message.type() === "error") consoleErrors.push(message.text()); });
      try {
        await page.goto(`http://127.0.0.1:${port}/.phase1b/deps/foliate-js/reader.html`, { waitUntil: "load" });
        await page.locator("#file-input").setInputFiles(path.resolve(epubArg));
        await page.waitForFunction(() => globalThis.reader?.view?.book && document.title && document.title !== "E-Book Reader", null, { timeout: 30000 });
        await page.waitForTimeout(1200);
        const frames = page.frames().filter(frame => frame !== page.mainFrame());
        let rendition = { text: "", lang: "", dir: "", images: 0, imagesComplete: 0, mathmlElements: 0, embeddedPdfElements: 0, links: 0 };
        for (const frame of frames) {
          try {
            const value = await frame.evaluate(() => ({
              text: document.body?.innerText || "", lang: document.documentElement.lang || "", dir: document.documentElement.dir || "",
              images: document.images.length, imagesComplete: [...document.images].filter(image => image.complete).length,
              mathmlElements: document.querySelectorAll("math").length,
              embeddedPdfElements: document.querySelectorAll('embed[type="application/pdf"],object[type="application/pdf"],iframe[src$=".pdf"]').length,
              links: document.links.length,
            }));
            if (value.text.length > rendition.text.length) rendition = value;
          } catch (_) {}
        }
        const book = await page.evaluate(() => ({
          title: document.title,
          dir: globalThis.reader.view.book.dir || "",
          sections: globalThis.reader.view.book.sections?.length || 0,
          navigationEntries: globalThis.reader.view.book.toc?.length || 0,
        }));
        const screenshot = representative.has(testId) ? path.join(screenshots, `${testId}.png`) : null;
        if (screenshot) await page.screenshot({ path: screenshot, fullPage: false });
        results.push({ testId, opened: true, ...book, ...rendition, textCharacters: rendition.text.length,
          arabicCharacters: (rendition.text.match(/[\u0600-\u06ff]/gu) || []).length,
          experimentalResourcesSurfaced: rendition.embeddedPdfElements > 0, consoleErrors,
          ...(screenshot ? { screenshot: path.relative(root, screenshot).replaceAll("\\", "/") } : {}) });
      } catch (error) {
        results.push({ testId, opened: false, error: String(error), consoleErrors });
      } finally { await page.close(); }
    }
  } finally { await browser.close(); await new Promise(resolve => server.close(resolve)); }
  const report = { reader: "Foliate JS", version: "git:78914aef4466eb960965702401634c2cb348e9b1", engine: "Chromium via Playwright", results };
  fs.writeFileSync(output, JSON.stringify(report, null, 2));
  process.stdout.write(JSON.stringify({ opened: results.filter(item => item.opened).length, total: results.length }));
}

main().catch(error => { console.error(error.stack || error); process.exit(1); });
