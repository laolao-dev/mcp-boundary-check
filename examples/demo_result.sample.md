# MCP Boundary Check local demo

Official MCP Python SDK 2.2.0; auto discovery; protocol 2026-07-28.

| Identity | Case | Expected | Actual | Handler records | PASS/FAIL |
| --- | --- | --- | --- | --- | --- |
| demo-readonly-token | readonly-write | DENY_AUTHORIZATION | DENY_AUTHORIZATION | 0 | PASS |
| demo-readonly-token | readonly-delete | DENY_AUTHORIZATION | DENY_AUTHORIZATION | 0 | PASS |
| demo-otheruser-token | cross-user-read | DENY_AUTHORIZATION | DENY_AUTHORIZATION | 0 | PASS |
| demo-admin-token | undeclared-argument | REJECT_SCHEMA | REJECT_SCHEMA | 0 | PASS |
| (none) | missing-token | DENY_AUTHENTICATION | DENY_AUTHENTICATION | 0 | PASS |
| demo-admin-token | admin-write | ALLOW | ALLOW | 1 | PASS |

Result: 6 PASS / 0 FAIL.
Audit: runtime JSONL is generated locally and is not included in this sample.

Fixture-only permission contracts, not third-party findings or full protocol certification.
Synthetic tokens in request metadata are not HTTP OAuth or production authentication.
