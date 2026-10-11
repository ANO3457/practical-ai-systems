import http from "node:http";
import fs from "node:fs";
import path from "node:path";
const PORT = Number(process.env.PORT) || 4173;
const ROOT = process.cwd();
const MIME = { ".html": "text/html", ".js": "text/javascript", ".json": "application/json", ".css": "text/css" };
const server = http.createServer((req, res) => {
  const url = (req.url || "/").split("?")[0];
  const filePath = path.join(ROOT, url === "/" ? "/index.html" : url);
  fs.readFile(filePath, (err, data) => {
    if (err) { res.writeHead(404); res.end("Not found"); return; }
    res.writeHead(200, { "Content-Type": MIME[path.extname(filePath)] || "application/octet-stream" });
    res.end(data);
  });
});
server.listen(PORT, () => console.log(`Serving on http://localhost:${PORT}`));
