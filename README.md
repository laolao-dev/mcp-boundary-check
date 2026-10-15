# MCP Boundary Check

A runnable, local MCP permission-contract demo built on the **official Python SDK 2.2.0**. Five requests must be denied; an admin write is the positive control. This is a portfolio/research demo, not a security certification or a scanner for third-party servers.

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

The command starts only its own stdio fixture, uses SDK auto discovery, requires negotiated protocol **2026-07-28**, lists the tools and sends all six calls. It prints a Markdown table and writes `demo_result.md`. A nonzero exit code means a failed case or execution error.

Expected table:

| Identity token | Case | Expected | Handler records |
| --- | --- | --- | --- |
| read-only | write_item | Denied | 0 |
| read-only | delete_item | Denied | 0 |
| other-user | Read admin's data | Denied | 0 |
| admin | Undeclared tool argument | Rejected | 0 |
| none | Missing token | Denied | 0 |
| admin | write_item | Allowed | 1 |

## Tests

With pytest already available in your development environment:

```powershell
python -m pytest -q
```

The six parametrized tests use the same cases through a real SDK client and fixture. No pytest plugin is required. Each test run uses a temporary audit path.

## How the evidence works

- `core.py` adapts the protocol-independent W1 `PermissionCore`: validate arguments, resolve the principal on the server, authorize, then execute and count the operation.
- `fixture_server.py` adapts W1's official SDK Server. The SDK owns discovery, schemas, JSON-RPC and stdio lifecycle. Tools are `read_item`, `write_item`, and `delete_item`.
- `client.py` adapts W1's SDK Client/stdio transport. It sends each case, including unauthorized ones; it does not block them locally. SDK context managers close the child process; requests time out after 10 seconds, and the demo has a 60-second timeout.
- Public synthetic tokens `admin`, `read-only`, and `other-user` travel in request `_meta.demo_token`. The fixture maps them to identities and roles; caller-supplied owner fields cannot grant access. Admin and read-only share the admin tenant; other-user has its own data. These tokens are **only local demo credentials**, not production authentication, stdio process identity or HTTP OAuth.
- Only entry into an authorized operation writes a JSONL line to the unique `artifacts/demo-*.jsonl` path. Denied cases must have zero matching entries; the successful write proves logging is active and checks handler/side-effect counters. Request correlation uses `_meta.demo_case`; tokens are not logged. An existing audit file is never truncated.

No Windows Job Object, observer, paid API or external server is used. The audit proves this fixture's instrumented behavior; it cannot establish zero side effects in an uninstrumented third-party server.

## Earlier research

`docs/` contains the historical 20-threat-model and design snapshot. Its old Gate statuses describe that publication baseline, not this demo. The W1 SDK adapter/core/client were the implementation basis; the old hand-written fixture and runner were not used. Prior research files and local evidence remain unchanged. See `RIGHTS.md` for the repository's existing rights statement.
