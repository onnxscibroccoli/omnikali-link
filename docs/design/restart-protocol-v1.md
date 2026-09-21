# Restart protocol v1

When a remote Kali origin is off, the workstation does **not** fail closed.
The local XFCE session stays up. Power, wake, and pointer-sync agents run this
sequence against the same NodeContract used for 1 → 1,028.

## Sequence

1. **detect** — record node state and last known origin.
2. **reprobe** — live health check of GitHub `omnikali.json` pointer + `/api/desktop`.
3. **wake** — if still dead, issue a wake ticket (`protocol/wake.schema.json`).
4. **reboot-local** — NodeContract `OFFLINE → ONLINE → READY` on `local://`.
   Headless tasks keep working. The desktop never waits on RFB.
5. **await-origin** — exponential backoff probes (400ms, 800ms, 1600ms).
6. **attached** if the tunnel returns, else **local-only** with the wake ticket outstanding.

`main` pointer (`omnikali.json`) is not mutated by this protocol.

## Triggers

- Boot: origin fail-closed → one automatic restart attempt.
- UI: **Restart remote** / panel **Wake**.
- Shell: `systemctl restart omnikali-remote` or `omnikali restart`.

## What this does not claim

A GitHub ticket cannot power on a machine that has no always-on helper.
If you run a WoL gateway or a second host, consume `wake.json` and send magic packets there. Until then the in-browser node is the live workstation.
