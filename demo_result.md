# MCP Boundary Check local demo

Official MCP Python SDK 2.2.0; auto discovery; protocol 2026-07-28.

| Identity | Case | Expected | Actual | Handler records | PASS/FAIL |
| --- | --- | --- | --- | --- | --- |
| read-only | readonly-write | DENY_AUTHORIZATION | DENY_AUTHORIZATION | 0 | PASS |
| read-only | readonly-delete | DENY_AUTHORIZATION | DENY_AUTHORIZATION | 0 | PASS |
| other-user | cross-user-read | DENY_AUTHORIZATION | DENY_AUTHORIZATION | 0 | PASS |
| admin | undeclared-argument | REJECT_SCHEMA | REJECT_SCHEMA | 0 | PASS |
| (none) | missing-token | DENY_AUTHENTICATION | DENY_AUTHENTICATION | 0 | PASS |
| admin | admin-write | ALLOW | ALLOW | 1 | PASS |

Result: 6 PASS / 0 FAIL.
Audit: `artifacts/demo-73f8140726dc407cac9b68e5141a31af.jsonl`

Fixture-only permission contracts, not third-party findings or full protocol certification.
Synthetic tokens in request metadata are not HTTP OAuth or production authentication.
