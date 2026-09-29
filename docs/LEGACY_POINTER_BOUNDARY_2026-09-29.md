# Legacy pointer boundary

omnikali-link is a legacy presentation and routing surface. It is not the workstation, gateway, authentication layer, or QEMU implementation.

The checked-in origin record may contain historical tunnel data. That data must not be promoted to a current production endpoint without a fresh external health probe.

## Rule

A future change may only publish an origin when:

1. the target uses HTTPS;
2. an external probe returns the expected health contract;
3. the endpoint is recorded with a timestamp;
4. the change does not alter the protected CloudFront -> nginx -> Helix path.

When the target is unavailable, the correct user-facing behavior is fail closed, not a stale redirect.
