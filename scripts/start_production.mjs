import { createReadStream, existsSync, statSync } from "node:fs";
import { createServer, get, request } from "node:http";
import { extname, join, resolve, sep } from "node:path";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const root = resolve(fileURLToPath(new URL("..", import.meta.url)));
const standalone = join(root, "dist", "standalone", "server.js");
const client = resolve(root, "dist", "standalone", "dist", "client");
const port = Number.parseInt(process.env.PORT ?? "3000", 10);
const host = process.env.HOST ?? "0.0.0.0";
const internalPort = Number.parseInt(process.env.VINEXT_INTERNAL_PORT ?? String(port + 1), 10);

if (!existsSync(standalone) || !existsSync(client)) {
  throw new Error("Missing standalone build. Run `pnpm build` before `pnpm start`.");
}

const child = spawn(process.execPath, [standalone], {
  cwd: root,
  env: { ...process.env, PORT: String(internalPort), HOST: "127.0.0.1" },
  stdio: "inherit",
});

const contentTypes = {
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
};

function staticPath(url) {
  let pathname;
  try { pathname = decodeURIComponent(new URL(url, "http://localhost").pathname); }
  catch { return null; }
  if (pathname === "/") return null;
  const candidate = resolve(client, `.${pathname}`);
  if (candidate !== client && !candidate.startsWith(client + sep)) return null;
  return existsSync(candidate) && statSync(candidate).isFile() ? candidate : null;
}

function waitForInternal(attempt = 0) {
  return new Promise((resolveReady, rejectReady) => {
    const probe = get(`http://127.0.0.1:${internalPort}/`, response => {
      response.resume();
      resolveReady();
    });
    probe.on("error", error => {
      if (attempt >= 50) rejectReady(error);
      else setTimeout(() => waitForInternal(attempt + 1).then(resolveReady, rejectReady), 100);
    });
  });
}

await waitForInternal();

const server = createServer((incoming, outgoing) => {
  const file = staticPath(incoming.url ?? "/");
  if (file) {
    outgoing.writeHead(200, {
      "Content-Type": contentTypes[extname(file)] ?? "application/octet-stream",
      "Content-Length": statSync(file).size,
      "Cache-Control": file.includes(`${sep}assets${sep}`) ? "public, max-age=31536000, immutable" : "public, max-age=3600",
    });
    createReadStream(file).pipe(outgoing);
    return;
  }
  const proxy = request({
    hostname: "127.0.0.1",
    port: internalPort,
    path: incoming.url,
    method: incoming.method,
    headers: incoming.headers,
  }, response => {
    outgoing.writeHead(response.statusCode ?? 500, response.headers);
    response.pipe(outgoing);
  });
  proxy.on("error", error => {
    outgoing.writeHead(502, { "Content-Type": "text/plain; charset=utf-8" });
    outgoing.end(`Production proxy error: ${error.message}`);
  });
  incoming.pipe(proxy);
});

server.listen(port, host, () => console.log(`Economic War Room production server: http://${host}:${port}`));

function shutdown() {
  server.close(() => child.kill());
}
process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);
child.on("exit", code => {
  if (code && code !== 0) process.exitCode = code;
});
