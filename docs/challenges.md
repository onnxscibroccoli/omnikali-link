# Ongoing challenges (workspace, 2026-09-21)

Lived issues from the in-browser workstation, not a wish list.

## Open

1. **Preview host 521** — Cloudflare reports the preview origin down even
   when the local XFCE session is healthy. The desktop must never wait on
   that tunnel. Restart protocol exists; the remote VNC origin is still
   often missing.

2. **Third-party iframes are blank** — Direct `src=https://duckduckgo.com`
   (and similar) shows a broken-document icon in mobile Chrome. Cause:
   `X-Frame-Options` / CSP `frame-ancestors` plus the preview embedding
   itself. Fix in tree: default Firefox to `/api/uplink?url=` (same-origin
   proxy). Direct tab remains for debugging and usually fails.

3. **DuckDuckGo unreachable from this node** — HEAD/GET to
   `duckduckgo.com` / `html.duckduckgo.com` time out. Bing, Wikipedia,
   example.com, and kali.org respond. Firefox rewrites DDG → Bing so the
   search bar is not a blank page.

4. **No nested Kali kernel** — The shell is a real interpreter with a
   virtual FS, not `/bin/bash` on a Kali VM. `nmap`/`msf`/`sqlmap` against
   the public internet cannot be made real here, and will not be enabled
   as a public scanner. Authorized tests on equipment you own belong on a
   machine you control.

5. **JS-heavy sites** — Proxied HTML with a `<base href>` still drops
   sites that require first-party cookies, service workers, or strict
   script nonces. Snapshot (srcDoc) is a fallback, not a full browser
   engine.

6. **ICMP / raw sockets** — `ping` is HTTPS HEAD over the uplink. There
   is no kernel ping.

7. **Remote desktop attach** — Gateway stays fail-closed until a live
   origin health-checks. Pointer
   (`onnxscibroccoli/omnikali-link` `omnikali.json`) and Cloudflare
   tunnels go stale; wake tickets do not power a machine that is actually
   off.

8. **Mobile window chrome** — A maximized terminal used to eat the whole
   viewport. Desktop-first boot (no auto-open terminal) is the current
   rule. Panel titles must stay visible on ~390px.

## Closed (this cycle)

- Local desktop independent of gateway (fail-open workstation).
- Public HTTPS uplink for curl / wget / ping / Firefox.
- Restart protocol + power / wake agents.
- Same-origin Firefox uplink proxy.
- docs-sync agent and this documentation set.

## Will not do

- Public-internet nmap, masscan, metasploit, sqlmap, gobuster, or nikto.
  Ownership claims in chat are not authorization we can verify, and this
  node has no raw sockets anyway.
