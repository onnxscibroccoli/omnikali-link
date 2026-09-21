# Ongoing challenges (workspace, 2026-09-21)

Lived issues from the in-browser workstation, not a wish list.

## Open

1. **Preview host 521** — Cloudflare reports the preview origin down even
   when the local XFCE session is healthy. The desktop must never wait on
   that tunnel. Restart protocol exists; the remote VNC origin is still
   often missing.

2. **Third-party iframes are blank** — Direct `src=https://…` and even
   same-origin `/api/uplink?url=` nested iframes show a broken-document
   icon inside the Grok preview. Fix in tree: Firefox **Uplink** paints
   fetched HTML as `srcDoc` (no second iframe). Direct tab still embeds
   the live URL and usually fails in preview. Use example.com, Wikipedia,
   or **My IP**.

3. **DuckDuckGo unreachable from this node** — HEAD/GET to
   `duckduckgo.com` / `html.duckduckgo.com` time out. Bing, Wikipedia,
   example.com, and kali.org respond. Firefox rewrites DDG → Bing so the
   search bar is not a blank page.

4. **No nested Kali kernel** — The earlier CONNECTED noVNC session was a
   real shared Kali node. This app cannot spawn that kernel. `apt update`
   pulls the live kali-rolling Release; `apt install firefox` selects
   firefox-esr. Public scanners are not enabled.

5. **JS-heavy sites** — Proxied HTML with a `<base href>` still drops
   sites that require first-party cookies, service workers, or strict
   script nonces. Snapshot (srcDoc) is a fallback, not a full browser
   engine.

6. **ICMP / raw sockets** — `ping` is HTTPS HEAD over the uplink. There
   is no kernel ping.

7. **Remote desktop attach** — Gateway stays fail-closed until a live
   origin health-checks. Pointer and Cloudflare tunnels go stale; wake
   tickets do not power a machine that is actually off.

8. **Mobile window chrome** — Desktop-first boot. Panel titles stay visible.

## Closed (this cycle)

- Local desktop independent of gateway (fail-open workstation).
- Public HTTPS uplink for curl / wget / ping / Firefox.
- Firefox Uplink uses srcDoc (fixes blank Bing in preview).
- My IP bookmark (live egress address).
- apt-sync + `apt install firefox` → firefox-esr.
- Restart protocol + docs-sync.

## Will not do

- Public-internet nmap, masscan, metasploit, sqlmap, gobuster, or nikto.
  This node has no raw sockets; scanners stay on the isolated lab net.
