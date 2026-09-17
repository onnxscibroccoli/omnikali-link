# Gateway & Discovery — Health-Aware Registration

## Stable entrypoint
Public stable URL (existing Vercel reverse-proxy / omnikali.json origin pointer).

## Dynamic origin
- omnikali.json remains the live origin pointer.
- Middleware continues origin validation + health checking.

## Registration rules
1. Discover candidate preview endpoint (e.g. ephemeral HDS ingress).
2. Validate health/readiness.
3. Only advertise if healthy.
4. Fail closed on dead HDS ports.

## Existing behavior to preserve
- omnikali.json dynamic URL pointer.
- middleware.js origin validation/health checking.
- Do not break the current reverse-proxy setup.
