# Upstream Tracking

## Repositories

- Upstream: https://github.com/wzdnzd/aggregator
- EasyProxy fork: https://github.com/aiaimimi0920/aggregator
- Root integration path: upstreams/aggregator

## Baseline

- Audited upstream main: 27daeb847cfdcf8f7675d701b419cc420739db74
- EasyProxy integration branch: main

The integration branch carries EasyProxy-specific crawler, liveness, workflow,
protocol, and regression hardening. It is intentionally pinned by the
EasyProxy root repository.

## EasyProxy Delta

- Safer crawler concurrency and source filtering.
- XHTTP, SOCKS, location, renewal, push, and workflow fixes.
- Stable R2-oriented publication integration.
- Regression coverage in tests/test_regressions.py.
- Root-monorepo configuration and verification contracts.

## Nested Submodule

The upstream manager dependency remains declared as a nested public submodule.
Root consumers must clone with recursive submodules enabled.

## Sync Policy

1. Fetch upstream into a dedicated sync branch.
2. Merge or cherry-pick upstream changes without dropping EasyProxy tests.
3. Review crawler, protocol, liveness, and publication behavior explicitly.
4. Run the fork regression suite and root Aggregator contract checks.
5. Update the EasyProxy root submodule pointer only after artifacts verify.

Never publish an untested upstream main commit directly as the stable artifact
producer.
