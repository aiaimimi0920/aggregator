# Upstream Tracking

## Repositories

- Upstream: https://github.com/wzdnzd/aggregator
- EasyProxy fork: https://github.com/aiaimimi0920/aggregator
- Root integration path: upstreams/aggregator

## Baseline

- Audited upstream main: d7fd6e0653e295ba05d42e1d4c604f0e29c6c54f
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
- Typed configuration compatibility for existing domains/sub, crawler settings,
  and R2 storage credentials and publication metadata.

## 2026-10-02 Integration Verification

- Merged the upstream typed configuration, crawler packages, and protocol modules.
- Retained EasyProxy R2 S3 and authenticated Worker upload paths, free-plan
  selection, source filtering, and workflow liveness fixes.
- All 16 fork regression tests pass. The root configuration loads through the
  actual process entrypoint with 2 sites, 3 Telegram channels, and 8 R2 items.
- Legacy publication workflows remain disabled; stable promotion is owned by the
  root deployment workflow and remains subject to its live artifact audit.

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
