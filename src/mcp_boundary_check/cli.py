"""One-command local demo."""
import argparse
import asyncio
from pathlib import Path
import sys
import uuid

from .client import run_demo, markdown


def main():
    parser = argparse.ArgumentParser(prog="python -m mcp_boundary_check")
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("run")
    run.add_argument("--demo", action="store_true", required=True)
    args = parser.parse_args()
    audit_path = Path("artifacts") / ("demo-" + uuid.uuid4().hex + ".jsonl")
    try:
        results = asyncio.run(run_demo(audit_path))
        report = markdown(results, audit_path)
        code = int(not all(r["passed"] for r in results))
    except Exception as exc:
        report = f"# MCP Boundary Check local demo\n\nERROR: {type(exc).__name__}: {exc}\n"
        code = 1
    Path("demo_result.md").write_text(report, encoding="utf-8")
    print(report)
    return code
