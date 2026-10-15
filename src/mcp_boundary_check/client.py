"""Real SDK client: send every case to the server, then inspect its audit log."""
import asyncio
from contextlib import asynccontextmanager
from importlib.metadata import version
import json
import os
from pathlib import Path
import sys

from mcp import Client, StdioServerParameters
from mcp.client.stdio import stdio_client

CASES = (
    ("readonly-write", "read-only", "write_item",
     {"owner": "admin", "key": "note", "value": "forbidden"}, "DENY_AUTHORIZATION"),
    ("readonly-delete", "read-only", "delete_item",
     {"owner": "admin", "key": "note"}, "DENY_AUTHORIZATION"),
    ("cross-user-read", "other-user", "read_item",
     {"owner": "admin", "key": "note"}, "DENY_AUTHORIZATION"),
    ("undeclared-argument", "admin", "write_item",
     {"owner": "admin", "key": "note", "value": "forbidden", "unexpected": True},
     "REJECT_SCHEMA"),
    ("missing-token", None, "write_item",
     {"owner": "admin", "key": "note", "value": "forbidden"}, "DENY_AUTHENTICATION"),
    ("admin-write", "admin", "write_item",
     {"owner": "admin", "key": "note", "value": "demo-written"}, "ALLOW"),
)


async def run_demo(audit_path):
    if version("mcp") != "2.2.0":
        raise RuntimeError("This demo requires the installed official mcp==2.2.0")
    audit_path = Path(audit_path).resolve()
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    # Never truncate an existing audit trail.
    audit_path.touch(exist_ok=False)
    params = StdioServerParameters(
        command=sys.executable,
        args=["-B", "-m", "mcp_boundary_check.fixture_server"],
        cwd=Path.cwd(),
        env={"MBC_DEMO_AUDIT": str(audit_path),
             "PYTHONPATH": os.pathsep.join(str(Path(p).resolve()) for p in sys.path if p)},
    )

    @asynccontextmanager
    async def transport():
        async with stdio_client(params) as streams:
            yield streams

    results = []
    client = Client(transport(), read_timeout_seconds=10)
    async with asyncio.timeout(60):
        async with client:
            if client.protocol_version != "2026-07-28" or client.session.discover_result is None:
                raise RuntimeError("Expected auto discovery with protocol 2026-07-28")
            listing = await client.list_tools()
            from .core import SCHEMAS
            if {t.name: t.input_schema for t in listing.tools} != SCHEMAS:
                raise RuntimeError("Fixture tool schemas do not match")
            for case_id, token, tool, arguments, expected in CASES:
                meta = {"demo_case": case_id}
                if token is not None:
                    meta["demo_token"] = token
                response = await client.call_tool(tool, arguments, meta=meta)
                data = response.structured_content or {}
                events = [json.loads(line) for line in audit_path.read_text(
                    encoding="utf-8").splitlines()]
                matching = [event for event in events if event.get("case_id") == case_id]
                allow = expected == "ALLOW"
                oracle = (len(matching) == int(allow))
                if allow:
                    oracle = oracle and data.get("value") == "demo-written" and (
                        data.get("handler_count"), data.get("side_effect_count")) == (1, 1)
                    oracle = oracle and matching[0]["tool"] == tool
                else:
                    oracle = oracle and not events  # all denials precede the positive control
                passed = (data.get("decision") == expected and
                          bool(response.is_error) == (not allow) and oracle)
                results.append({
                    "case": case_id, "identity": token or "(none)", "tool": tool,
                    "expected": expected, "actual": data.get("decision", "MISSING"),
                    "handler_records": len(matching), "passed": passed,
                })
    if client._session is not None:
        raise RuntimeError("SDK client session did not close")
    return results


def markdown(results, audit_path):
    lines = ["# MCP Boundary Check local demo", "",
             "Official MCP Python SDK 2.2.0; auto discovery; protocol 2026-07-28.",
             "", "| Identity | Case | Expected | Actual | Handler records | PASS/FAIL |",
             "| --- | --- | --- | --- | --- | --- |"]
    for r in results:
        lines.append("| {identity} | {case} | {expected} | {actual} | {handler_records} | "
                     "{status} |".format(**r, status="PASS" if r["passed"] else "FAIL"))
    passed = sum(r["passed"] for r in results)
    lines += ["", f"Result: {passed} PASS / {len(results) - passed} FAIL.",
              f"Audit: `{Path(audit_path).as_posix()}`", "",
              "Fixture-only permission contracts, not third-party findings or full protocol certification.",
              "Synthetic tokens in request metadata are not HTTP OAuth or production authentication."]
    return "\n".join(lines) + "\n"

