"""Eight permission contracts through SDK fixtures, in forward and reverse order."""
import asyncio
import json

import pytest

from mcp_boundary_check.client import CASES, run_demo


@pytest.fixture(scope="module")
def observed(tmp_path_factory):
    runs = []
    for label, cases in (("forward", CASES), ("reverse", tuple(reversed(CASES)))):
        path = tmp_path_factory.mktemp("mbc-" + label) / "audit.jsonl"
        results = asyncio.run(run_demo(path, cases=cases))
        events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        runs.append(({result["case"]: result for result in results}, events))
    return runs


@pytest.mark.parametrize("index", range(len(CASES)), ids=[case[0] for case in CASES])
def test_permission_contract(observed, index):
    case_id, token, tool, arguments, expected = CASES[index]
    for results, events in observed:
        result = results[case_id]
        assert result["identity"] == (token or "(none)")
        assert token is None or token in {
            "demo-admin-token", "demo-readonly-token", "demo-otheruser-token"
        }
        assert result["passed"], result
        matching = [event for event in events if event["case_id"] == case_id]
        if expected == "ALLOW":
            assert len(matching) == 1
            assert matching[0]["principal"] == arguments["owner"]
            assert matching[0]["tool"] == tool
        else:
            assert matching == []
        assert len(events) == sum(case[4] == "ALLOW" for case in CASES)
