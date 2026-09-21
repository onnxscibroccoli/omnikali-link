# Ongoing challenges (workspace)

Recorded from the Grok Build workstation session, 2026-09-21.

1. **Preview host 521** — Cloudflare in front of the Grok preview returns 521 when the origin process is down. The local XFCE session must stay usable without that origin.
2. **Third-party iframes fail** — DuckDuckGo (and most major sites) render as a blank broken document when loaded as `iframe src=https://…` inside the preview. Firefox must use the same-origin uplink.
3. **DuckDuckGo is unreachable from this node** — `duckduckgo.com` / `html.duckduckgo.com` time out. Wikipedia, Kali docs, Bing, example.com succeed. Address-bar search uses Bing until DDG is reachable.
4. **Remote desktop origin is often dead** — pointer `omnikali.json` and the Cloudflare tunnel probe fail closed. Restart protocol keeps the local session; it cannot power-on a machine that has no wake channel.
5. **No nested Kali kernel** — no real ICMP, no raw sockets, no apt that mutates a distro. ping is HTTPS RTT. nmap of public space stays closed.
6. **HMR / node builtins** — `node:dns` in a route module 500s the entire app in Vite SSR. Uplink uses URL/host checks only.
7. **Control-plane vs workstation** — earlier builds showed 3 READY nodes and Gateway closed. That is not a desktop. The workstation is the desktop; the fleet is optional.
