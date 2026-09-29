# omnikali-link

**Status:** Public pointer/phone shell; legacy boundary  
**Repository:** `onnxscibroccoli/omnikali-link`  
**Documentation snapshot:** 2026-09-28 23:12 EDT

This repository provides the public `omnikali.vercel.app` entry surface and points it at the currently published OmniKali origin.

It is intentionally small. It is **not the Kali VM, not the gateway implementation, and not the current workstation source**.

## Contents

Six tracked files form the pointer application:

- `index.html` — public shell.
- `middleware.js` — request/origin behavior.
- `omnikali.json` — current origin record.
- `vercel.json` — deployment configuration.
- `favicon.svg` — icon.
- `README.md` — documentation.

Recent commits show the shell evolving from a simple pointer into a fail-fast phone-oriented surface that probes candidate origins without waiting indefinitely.

## Development cycle

**MAINTENANCE / LEGACY POINTER.**

The repository still has a useful public entry-point role, but newer OmniKali work uses the GitHub Pages stable-door model and the workstation/control-plane repositories.

Do not expand this repository into the workstation itself.

## How to use it

Inspect the deployment:

```bash
git clone https://github.com/onnxscibroccoli/omnikali-link.git
cd omnikali-link
cat omnikali.json
```

The Vercel project is intended to serve the public phone shell.

## AI model instructions

An AI should treat this repository as a **routing/presentation boundary**.

Do not put VM logic, QEMU management, authentication policy, or RFB implementation here.

If changing origin-selection logic, fail closed when the target is unavailable. Never redirect users to a stale or unverified origin merely because a hostname exists.

For current workstation behavior, inspect `kali-node`, `omnikali`, Helix, and Grasshopper before changing this project.

**Bottom line:** a small public pointer/shell whose job is to get the user to a verified OmniKali entry point, not to implement OmniKali itself.
