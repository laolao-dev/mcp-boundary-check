"""Six permission contracts through the official client and local SDK fixture."""
import asyncio
import json

import pytest

from mcp_boundary_check.client import CASES, run_demo


@pytest.fixture(scope="module")
def observed(tmp_path_factory):
    path = tmp_path_factory.mktemp("mbc-demo") / "audit.jsonl"
    results = asyncio.run(run_demo(path))
    return results, [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


@pytest.mark.parametrize("index", range(len(CASES)), ids=[case[0] for case in CASES])
def test_permission_contract(observed, index):
    results, events = observed
    result = results[index]
    assert result["identity"] == (CASES[index][1] or "(none)")
    assert CASES[index][1] is None or CASES[index][1] in {
        "demo-admin-token", "demo-readonly-token", "demo-otheruser-token"
    }
    assert result["passed"], result
    matching = [event for event in events if event["case_id"] == result["case"]]
    if result["expected"] == "ALLOW":
        assert len(matching) == 1
        assert matching[0]["principal"] == "admin"
        assert matching[0]["tool"] == "write_item"
    else:
        assert matching == []
    assert len(events) == 1  # positive control proves audit logging is active
