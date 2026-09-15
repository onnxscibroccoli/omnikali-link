export const config = { matcher: ["/origin.json"] };

const FALLBACK = "https://alcohol-sand-dispatched-easily.trycloudflare.com";
const POINTER = "https://raw.githubusercontent.com/onnxscibroccoli/omnikali-link/main/omnikali.json";
const DENY = new Set([
  "api.trycloudflare.com",
  "www.trycloudflare.com",
  "dash.cloudflare.com",
  "console.serveo.net",
]);

function okOrigin(value) {
  try {
    const u = new URL(value);
    if (u.protocol !== "https:") return false;
    const host = u.hostname.toLowerCase();
    if (DENY.has(host) || host.startsWith("api.") || host.startsWith("www.")) return false;
    return host.endsWith(".trycloudflare.com") || host.endsWith(".serveousercontent.com") || host.endsWith(".serveo.net") || host.endsWith(".localhost.run") || host.endsWith(".lhr.life") || host.endsWith(".pinggy.io") || host.endsWith(".loca.lt");
  } catch {
    return false;
  }
}

async function live(url) {
  try {
    const ac = new AbortController();
    const timer = setTimeout(() => ac.abort(), 700);
    const res = await fetch(url + "/api/desktop", { method: "HEAD", cache: "no-store", signal: ac.signal, headers: { Accept: "image/jpeg" } });
    clearTimeout(timer);
    const type = res.headers.get("content-type") || "";
    return res.status === 304 || (res.ok && type.includes("image"));
  } catch {
    return false;
  }
}

export default async function middleware() {
  const cands = [];
  const ac = new AbortController();
  const timer = setTimeout(() => ac.abort(), 800);
  try {
    const res = await fetch(POINTER, { cache: "no-store", signal: ac.signal });
    const body = await res.json();
    if (okOrigin(body.url)) cands.push(String(body.url).replace(/\/$/, ""));
  } catch {
    /* FALLBACK */
  } finally {
    clearTimeout(timer);
  }
  if (okOrigin(FALLBACK)) cands.push(FALLBACK);
  const uniq = [...new Set(cands)];
  let origin = null;
  for (const c of uniq) {
    if (await live(c)) { origin = c; break; }
  }
  if (!origin) origin = uniq.find((c) => c === FALLBACK) || uniq[0] || null;
  if (!okOrigin(origin)) {
    return new Response(JSON.stringify({ name: "omnikali", url: null }), {
      status: 503,
      headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", "access-control-allow-origin": "*" },
    });
  }
  return new Response(JSON.stringify({ name: "omnikali", url: origin }), {
    status: 200,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", "access-control-allow-origin": "*" },
  });
}
