# OmniKali workstation

In-browser Kali XFCE session. The local desktop is the product. A remote origin is optional.

## Surfaces

- **Desktop** — wallpaper, panel, icons, windows. Always boots. Never waits on RFB.
- **Firefox ESR** — public pages load through the same-origin HTTPS uplink (`/api/uplink?url=`), not a third-party iframe. Direct embeds are blocked by the preview host.
- **QTerminal** — zsh-shaped builtins. `curl` / `wget` / `ping` use the live uplink. Lab HTTP still hits `10.10.10.0/24`.
- **GitHub** — reads `onnxscibroccoli/omnikali-link` pointer, lists repos, clones via the public API.
- **Remote Node** — attaches when `/api/desktop` is healthy. Restart protocol wakes/reboots when the origin is off. Fail-open locally if the tunnel is dead.

## Network split

| Path | Scope |
| --- | --- |
| Firefox, curl, wget, ping | Public HTTPS GET/HEAD. Private IPs and link-local blocked. |
| nmap, gobuster, sqlmap, nikto, msf | Isolated lab `10.10.10.0/24` only |
| GitHub | `api.github.com` |

Public scanning and exploit tooling stay lab-only. This is an in-browser workstation, not a nested kernel.

## Agents

supervisor, orchestrator, gateway-discovery, registry, verification, reservation, recovery, telemetry, desktop-session, shell, filesystem, github-link, lab-network, remote-desktop, power, wake, pointer-sync, public-uplink, docs-sync.

## Restart when the remote is off

`systemctl restart omnikali-remote` / Wake: detect → reprobe → wake ticket → reboot local contract → await origin → attached or local-only.
