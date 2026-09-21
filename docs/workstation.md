# OmniKali workstation — how it works

OmniKali is an **in-browser Kali XFCE desktop**. The desktop is local and
always on. A remote VNC origin is optional. A live HTTPS uplink reaches the
public internet for browsing and GET/HEAD.

## Layers

| Layer | What it is | Fail mode |
|---|---|---|
| Local XFCE | Wallpaper, panel, windows, Terminal, Firefox, Files, GitHub | Always boots |
| NodeContract | One interface for 1 → 1,028 nodes (`OFFLINE → ONLINE → READY`) | Watchdog TTL |
| Restart protocol | Detect → probe → wake ticket → reboot-local → await origin | Local-only if origin is off |
| Public uplink | Server-side HTTPS GET/HEAD, SSRF-guarded | Private hosts blocked |
| Firefox ESR | Same-origin `/api/uplink?url=` (not a third-party iframe) | Direct embed often blank |
| Lab net `10.10.10.0/24` | DVWA, web01, dc01, scanners (nmap, msf, gobuster, sqlmap, nikto) | Isolated range |

## Public internet (live)

- Firefox **Uplink** tab loads `GET /api/uplink?url=` so the preview cannot be
  blocked by `X-Frame-Options`.
- `curl`, `wget`, and `ping` use the same uplink (HTTPS, not ICMP).
- Search terms in Firefox go to Bing. DuckDuckGo is rewritten to Bing because
  that host times out from this node.
- SSRF guard: no `localhost`, RFC1918, link-local, or userinfo URLs.
- Cap: ~900 KB body, 12 s timeout, 5 redirects.

## What this is not

This is **not** a nested Kali kernel. There are no raw sockets, no real ICMP,
and no public-network scanner. Attack tools stay on the isolated lab. A box
you own running real Kali is the place for authorized tests against hosts
you actually control.

## Restart when a remote machine is off

`systemctl restart omnikali-remote` / `omnikali restart` / the Wake control:

1. **detect** — node state
2. **reprobe** — health check the advertised origin
3. **wake** — issue a wake ticket
4. **reboot-local** — `NodeContract.reboot()`
5. **await-origin** — wait for a live origin
6. **attached** or **local-only** — desktop stays usable either way

A Cloudflare 521 on a tunnel does not take the local workstation down.

## Agents

supervisor, orchestrator, gateway-discovery, registry, verification,
reservation, recovery, telemetry, desktop-session, shell, filesystem,
github-link, lab-network, remote-desktop, power, wake, pointer-sync,
public-uplink, docs-sync.

Pointer: `https://raw.githubusercontent.com/onnxscibroccoli/omnikali-link/main/omnikali.json`
