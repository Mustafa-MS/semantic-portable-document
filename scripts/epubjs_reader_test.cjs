const fs = require("fs");
const http = require("http");
const path = require("path");
const { chromium } = require("playwright");

async function main() {
  const [workspaceArg, outputArg, screenshotDirArg, chromeArg, epubjsArg, jszipArg, ...epubArgs] = process.argv.slice(2);
  if (!epubArgs.length) throw new Error("no EPUB inputs");
  const root = path.resolve(workspaceArg);
  const output = path.resolve(outputArg);
  const screenshots = path.resolve(screenshotDirArg);
  fs.mkdirSync(path.dirname(output), { recursive: true });
  fs.mkdirSync(screenshots, { recursive: true });
  const server = http.createServer((request, response) => {
    const rel = decodeURIComponent(new URL(request.url, "http://127.0.0.1").pathname).replace(/^\/+/, "");
    const target = path.resolve(root, rel);
    if (!target.startsWith(root) || !fs.existsSync(target) || !fs.statSync(target).isFile()) { response.writeHead(404); response.end(); return; }
    const type = target.endsWith(".epub") ? "application/epub+zip" : "application/octet-stream";
    response.writeHead(200, { "Content-Type": type, "Access-Control-Allow-Origin": "*", "Cache-Control": "no-store" });
    fs.createReadStream(target).pipe(response);
  });
  await new Promise(resolve => server.listen(0, "127.0.0.1", resolve));
  const port = server.address().port;
  const browser = await chromium.launch({ executablePath: path.resolve(chromeArg), headless: true });
  const results = [];
  try {
    for (const epubArg of epubArgs) {
      const epub = path.resolve(epubArg);
      const testId = path.basename(epub, ".epub");
      const page = await browser.newPage({ viewport: { width: 1100, height: 1250 }, deviceScaleFactor: 1 });
      const errors = [];
      page.on("console", message => { if (message.type() === "error") errors.push(message.text()); });
      page.on("pageerror", error => errors.push(error.message));
      await page.setContent('<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;background:#d8e0e3}#viewer{width:920px;height:1160px;margin:30px auto;background:white;box-shadow:0 2px 12px #789}</style></head><body><div id="viewer"></div></body></html>');
      await page.addScriptTag({ path: path.resolve(jszipArg) });
      await page.addScriptTag({ path: path.resolve(epubjsArg) });
      const relative = path.relative(root, epub).split(path.sep).map(encodeURIComponent).join("/");
      const url = `http://127.0.0.1:${port}/${relative}`;
      let observation;
      try {
        observation = await page.evaluate(async ({ url, testId }) => {
          const book = ePub(url, { openAs: "epub" });
          await book.ready;
          const navigation = await book.loaded.navigation;
          const rendition = book.renderTo("viewer", { width: 920, height: 1160, flow: "paginated", spread: "none" });
          await rendition.display();
          await new Promise(resolve => setTimeout(resolve, 900));
          const contents = rendition.getContents();
          const doc = contents[0]?.document;
          if (!doc) throw new Error("epub.js produced no content document");
          const images = [...doc.images];
          const result = {
            testId,
            opened: true,
            navigationEntries: navigation.toc?.length || 0,
            title: doc.title,
            lang: doc.documentElement.lang || doc.documentElement.getAttribute("xml:lang") || "",
            dir: doc.documentElement.dir || "",
            textCharacters: (doc.body?.innerText || "").length,
            arabicCharacters: ((doc.body?.innerText || "").match(/[\u0600-\u06ff]/g) || []).length,
            images: images.length,
            imagesComplete: images.filter(image => image.complete && image.naturalWidth > 0).length,
            mathmlElements: doc.getElementsByTagNameNS("http://www.w3.org/1998/Math/MathML", "math").length,
            links: doc.querySelectorAll("a[href]").length,
            embeddedPdfElements: doc.querySelectorAll('object[type="application/pdf"],embed[type="application/pdf"],iframe[src$=".pdf"]').length,
            renderedResource: contents[0].section?.href || "",
            experimentalResourcesSurfaced: /experimental\/(fixed|mapping|state)/.test(doc.body?.innerText || ""),
          };
          book.destroy();
          return result;
        }, { url, testId });
        if (["T01", "T04", "T05", "T08", "T09"].includes(testId)) {
          await page.screenshot({ path: path.join(screenshots, `${testId}.png`), fullPage: true });
          observation.screenshot = path.join("reports", "screenshots", "epubjs", `${testId}.png`).replaceAll("\\", "/");
        }
      } catch (error) {
        observation = { testId, opened: false, error: String(error) };
      }
      observation.consoleErrors = errors;
      results.push(observation);
      await page.close();
    }
  } finally {
    await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
  fs.writeFileSync(output, JSON.stringify({ reader: "epub.js", version: "0.3.93", engine: "Chromium via Playwright", results }, null, 2));
  process.stdout.write(JSON.stringify({ opened: results.filter(item => item.opened).length, total: results.length }));
}

main().catch(error => { console.error(error.stack || error); process.exit(1); });

