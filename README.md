# MCP Boundary Check

A runnable, local MCP permission-contract demo built on the **official Python SDK 2.2.0**. Five requests must be denied; two authorized reads and an admin write are positive controls. This is a portfolio/research demo, not a security certification or a scanner for third-party servers.

## Quick start

Python 3.11+ is required. From the repository root, use a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install "mcp==2.2.0"
$env:PYTHONPATH = "$PWD/src"
python -m mcp_boundary_check run --demo
```

On macOS/Linux, activate with `source .venv/bin/activate` and set `export PYTHONPATH="$PWD/src"` before the same run command. The source package uses Python's namespace-package support; no project build backend is needed.

The command starts only its own stdio fixture, uses SDK auto discovery, requires negotiated protocol **2026-07-28**, lists the tools and sends all eight calls. It prints a Markdown table and writes `demo_result.md`. Runtime reports and JSONL logs are ignored by Git; [examples/demo_result.sample.md](examples/demo_result.sample.md) is the single committed example. A nonzero exit code means a failed case or execution error.

Expected table:

| Identity token | Case | Expected | Handler records |
| --- | --- | --- | --- |
| demo-readonly-token | Read admin's note | Allowed | 1 |
| demo-readonly-token | write_item | Denied | 0 |
| demo-otheruser-token | Read own note | Allowed | 1 |
| demo-readonly-token | delete_item | Denied | 0 |
| demo-otheruser-token | Read admin's data | Denied | 0 |
| demo-admin-token | Undeclared tool argument | Rejected | 0 |
| none | Missing token | Denied | 0 |
| demo-admin-token | write_item | Allowed | 1 |

## Tests

With pytest already available in your development environment:

```powershell
python -m pytest -q
```

The eight parametrized tests use the same cases through real SDK clients and fresh fixtures, in both forward and reverse order. Each case checks only its own `case_id` audit records; total records must equal the three allowed cases. No pytest plugin is required. Each run uses a temporary audit path.

## How the evidence works

- `core.py` adapts the protocol-independent W1 `PermissionCore`: authenticate on the server, validate arguments, authorize, then execute and count the operation. Missing-token uses invalid arguments too: authentication must reject it before schema validation.
- `fixture_server.py` adapts W1's official SDK Server. The SDK owns discovery, schemas, JSON-RPC and stdio lifecycle. Tools are `read_item`, `write_item`, and `delete_item`.
- `client.py` adapts W1's SDK Client/stdio transport. It sends each case, including unauthorized ones; it does not block them locally. SDK context managers close the child process; requests time out after 10 seconds, and the demo has a 60-second timeout.
- Public synthetic tokens `demo-admin-token`, `demo-readonly-token`, and `demo-otheruser-token` travel in request `_meta.demo_token`. The fixture maps them to identities and roles; caller-supplied owner fields cannot grant access. Admin and read-only share the admin tenant; other-user has its own data. These tokens are **only local demo credentials**, not production authentication, stdio process identity or HTTP OAuth.
- Only entry into an authorized operation writes a JSONL line to the unique `artifacts/demo-*.jsonl` path. Denied cases must have zero entries for their own case ID; each allowed read/write must have exactly one. Checks do not depend on denied requests running first. Request correlation uses `_meta.demo_case`; tokens are not logged. An existing audit file is never truncated.

No Windows Job Object, observer, paid API or external server is used. The audit proves this fixture's instrumented behavior; it cannot establish zero side effects in an uninstrumented third-party server.

## Earlier research

`docs/` contains the historical 20-threat-model and design snapshot. [Historical validation](docs/history/VALIDATION.md) and [publication scope](docs/history/PUBLICATION_SCOPE.md) describe that old baseline, not this demo. The W1 SDK adapter/core/client were the implementation basis; the old hand-written fixture and runner were not used. Original local evidence remains read-only.

## License

Copyright 2026 LI JINYU. Licensed under [Apache-2.0](LICENSE); see [RIGHTS.md](RIGHTS.md) for third-party boundaries.
