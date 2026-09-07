/* Disposable Phase 1B adapter: source identity/ranges -> Paged.js page geometry + PDF. */
const fs = require("fs");
const http = require("http");
const path = require("path");
const { chromium } = require("playwright");

async function main() {
  const [sourceArg, pdfArg, rawMapArg, chromeArg, pagedPolyfillArg] = process.argv.slice(2);
  if (![sourceArg, pdfArg, rawMapArg, chromeArg, pagedPolyfillArg].every(Boolean)) {
    throw new Error("usage: node pagedjs_forward.cjs SOURCE PDF RAW_MAP CHROME PAGED_POLYFILL");
  }
  const source = path.resolve(sourceArg);
  const pdfPath = path.resolve(pdfArg);
  const rawMapPath = path.resolve(rawMapArg);
  fs.mkdirSync(path.dirname(pdfPath), { recursive: true });
  fs.mkdirSync(path.dirname(rawMapPath), { recursive: true });
  const root = process.cwd();
  const sourceRelative = path.relative(root, source);
  if (sourceRelative.startsWith("..") || path.isAbsolute(sourceRelative)) throw new Error("source must be inside workspace");
  const mime = { ".xhtml": "application/xhtml+xml", ".html": "text/html", ".css": "text/css", ".png": "image/png", ".svg": "image/svg+xml" };
  const server = http.createServer((request, response) => {
    const pathname = decodeURIComponent(new URL(request.url, "http://127.0.0.1").pathname).replace(/^\/+/, "");
    const target = path.resolve(root, pathname);
    if (!target.startsWith(root) || !fs.existsSync(target) || !fs.statSync(target).isFile()) {
      response.writeHead(404); response.end("not found"); return;
    }
    response.writeHead(200, { "Content-Type": mime[path.extname(target).toLowerCase()] || "application/octet-stream", "Access-Control-Allow-Origin": "*" });
    fs.createReadStream(target).pipe(response);
  });
  await new Promise(resolve => server.listen(0, "127.0.0.1", resolve));
  const address = server.address();
  const sourceUrl = `http://127.0.0.1:${address.port}/${sourceRelative.split(path.sep).map(encodeURIComponent).join("/")}`;
  const browser = await chromium.launch({ executablePath: path.resolve(chromeArg), headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
    await page.goto(sourceUrl, { waitUntil: "load" });
    await page.emulateMedia({ media: "print" });

    const catalog = await page.evaluate(() => {
      const ownerOffsets = new Map();
      const ownerExpected = new Map();
      const owners = [...document.querySelectorAll("[data-node-id]")];
      const catalog = {};
      for (const element of owners) {
        const id = element.getAttribute("data-node-id");
        const style = getComputedStyle(element);
        catalog[id] = {
          tag: element.localName,
          visibleInSourceLayout: style.display !== "none" && style.visibility !== "hidden",
          sourceText: "",
          expectedNonWhitespaceCharacters: 0,
          nonVisualNonWhitespaceCharacters: 0,
        };
        ownerOffsets.set(id, 0);
        ownerExpected.set(id, 0);
      }

      const textNodes = [];
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      while (walker.nextNode()) textNodes.push(walker.currentNode);
      for (const textNode of textNodes) {
        const parent = textNode.parentElement;
        const owner = parent && parent.closest("[data-node-id]");
        if (!owner || !textNode.nodeValue) continue;
        const id = owner.getAttribute("data-node-id");
        const value = textNode.nodeValue;
        let cursor = ownerOffsets.get(id) || 0;
        catalog[id].sourceText += value;
        const style = getComputedStyle(parent);
        const explicitlyNonVisual = Boolean(parent.closest('svg title, svg desc, [aria-hidden="true"], script, style, template'))
          || style.display === "none" || style.visibility === "hidden";
        if (explicitlyNonVisual) {
          catalog[id].nonVisualNonWhitespaceCharacters += (value.match(/\S/gu) || []).length;
          ownerOffsets.set(id, cursor + value.length);
          continue;
        }
        const fragment = document.createDocumentFragment();
        const parts = value.match(/\s+|\S+/gu) || [];
        for (const part of parts) {
          const start = cursor;
          const end = start + part.length;
          if (/\S/u.test(part)) {
            const span = document.createElement("span");
            span.className = "sf-map-token";
            span.setAttribute("data-map-owner", id);
            span.setAttribute("data-map-start", String(start));
            span.setAttribute("data-map-end", String(end));
            span.textContent = part;
            fragment.appendChild(span);
            ownerExpected.set(id, (ownerExpected.get(id) || 0) + part.length);
          } else {
            fragment.appendChild(document.createTextNode(part));
          }
          cursor = end;
        }
        ownerOffsets.set(id, cursor);
        textNode.replaceWith(fragment);
      }
      for (const [id, count] of ownerExpected) catalog[id].expectedNonWhitespaceCharacters = count;
      const markerStyle = document.createElement("style");
      markerStyle.textContent = ".sf-map-token{display:inline;padding:0;margin:0;border:0}";
      document.head.appendChild(markerStyle);
      return {
        nodes: catalog,
        documentId: document.querySelector('meta[name="document-id"]')?.content || "",
        revisionId: document.querySelector('meta[name="revision-id"]')?.content || "",
        title: document.title,
        lang: document.documentElement.lang || "",
        dir: document.documentElement.dir || "",
      };
    });

    await page.evaluate(() => { window.PagedConfig = { auto: false }; });
    await page.addScriptTag({ path: path.resolve(pagedPolyfillArg) });
    const started = Date.now();
    const preview = await page.evaluate(async () => {
      const content = document.body.innerHTML;
      const css = [...document.querySelectorAll('link[rel="stylesheet"]')].map(link => link.href);
      document.body.innerHTML = "";
      const previewer = new window.Paged.Previewer();
      const flow = await previewer.preview(content, css, document.body);
      return { total: flow.total, performance: flow.performance || null };
    });
    const paginationTimeMs = Date.now() - started;

    const raw = await page.evaluate((catalog) => {
      const pages = [...document.querySelectorAll(".pagedjs_page")];
      const blockFragments = [];
      const textFragments = [];
      const discardedOffPageFragments = [];
      const pageInfo = [];
      const round = value => Math.round(value * 1000) / 1000;
      const clipToSheet = (rect, sheetRect) => {
        const left = Math.max(rect.left, sheetRect.left), top = Math.max(rect.top, sheetRect.top);
        const right = Math.min(rect.right, sheetRect.right), bottom = Math.min(rect.bottom, sheetRect.bottom);
        return right > left && bottom > top ? [round(left - sheetRect.left), round(top - sheetRect.top), round(right - sheetRect.left), round(bottom - sheetRect.top)] : null;
      };
      for (let index = 0; index < pages.length; index++) {
        const page = pages[index];
        const sheet = page.querySelector(".pagedjs_pagebox") || page.querySelector(".pagedjs_sheet") || page;
        const sheetRect = sheet.getBoundingClientRect();
        const pageId = `pg_${index + 1}`;
        pageInfo.push({ id: pageId, widthCssPx: round(sheetRect.width), heightCssPx: round(sheetRect.height) });
        for (const element of page.querySelectorAll("[data-node-id]")) {
          const rect = element.getBoundingClientRect();
          const clipped = clipToSheet(rect, sheetRect);
          if (!clipped) {
            discardedOffPageFragments.push({ kind: "block", node: element.getAttribute("data-node-id"), page: pageId,
              rectCssPx: [round(rect.left - sheetRect.left), round(rect.top - sheetRect.top), round(rect.right - sheetRect.left), round(rect.bottom - sheetRect.top)] });
            continue;
          }
          blockFragments.push({
            node: element.getAttribute("data-node-id"), page: pageId,
            rectCssPx: clipped,
          });
        }
        for (const span of page.querySelectorAll("[data-map-owner]")) {
          const range = document.createRange();
          range.selectNodeContents(span);
          for (const rect of range.getClientRects()) {
            const clipped = clipToSheet(rect, sheetRect);
            if (!clipped) {
              discardedOffPageFragments.push({ kind: "text-range", node: span.getAttribute("data-map-owner"), page: pageId,
                logicalRange: [Number(span.getAttribute("data-map-start")), Number(span.getAttribute("data-map-end"))],
                rectCssPx: [round(rect.left - sheetRect.left), round(rect.top - sheetRect.top), round(rect.right - sheetRect.left), round(rect.bottom - sheetRect.top)] });
              continue;
            }
            textFragments.push({
              node: span.getAttribute("data-map-owner"), page: pageId,
              logicalRange: [Number(span.getAttribute("data-map-start")), Number(span.getAttribute("data-map-end"))],
              rectCssPx: clipped,
              renderedText: span.textContent,
            });
          }
        }
      }
      return { catalog, pages: pageInfo, blockFragments, textFragments, discardedOffPageFragments };
    }, catalog);
    raw.adapter = { method: "forward:pagedjs-dom", version: "0.4.3", paginationTimeMs, preview };
    fs.writeFileSync(rawMapPath, JSON.stringify(raw, null, 2));

    await page.addStyleTag({ content: `
      @media print {
        html, body { margin: 0 !important; padding: 0 !important; background: white !important; }
        .pagedjs_pages { display: block !important; }
        .pagedjs_page { margin: 0 !important; break-after: page !important; box-shadow: none !important; }
      }
    `});
    await page.pdf({ path: pdfPath, printBackground: true, preferCSSPageSize: true, displayHeaderFooter: false, tagged: true, outline: true });
    process.stdout.write(JSON.stringify({ pages: raw.pages.length, nodes: Object.keys(catalog.nodes).length, blockFragments: raw.blockFragments.length, textFragments: raw.textFragments.length, paginationTimeMs }));
  } finally {
    await browser.close();
    await new Promise(resolve => server.close(resolve));
  }
}

main().catch(error => { console.error(error.stack || error); process.exit(1); });
