import fs from "node:fs";
import { pathToFileURL } from "node:url";

const [pdfPath, pdfjsPath] = process.argv.slice(2);
if (!pdfPath || !pdfjsPath) throw new Error("usage: node pdfjs_extract.mjs PDF PDFJS_MJS");
const pdfjs = await import(pathToFileURL(pdfjsPath).href);
const data = new Uint8Array(fs.readFileSync(pdfPath));
const document = await pdfjs.getDocument({ data, disableWorker: true, useSystemFonts: true }).promise;
const pages = [];
for (let number = 1; number <= document.numPages; number++) {
  const page = await document.getPage(number);
  const content = await page.getTextContent();
  let text = "";
  for (const item of content.items) {
    if (!("str" in item)) continue;
    text += item.str;
    text += item.hasEOL ? "\n" : " ";
  }
  pages.push(text.trimEnd());
}
process.stdout.write(JSON.stringify({ pages, text: pages.join("\n") }));

