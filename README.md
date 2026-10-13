# MCP Boundary Check — research preview / design notes

This is a public documentation snapshot of early MCP/agent trust-boundary research. It contains 20 conditional threat hypotheses, scope and observation criteria, official reference links, and a proposed engineering gate protocol.

## Read the snapshot

Start with `docs/THREAT_MODEL_V2.md`, then `docs/ENGINEERING_GATE_PROTOCOL_V2.md`. `docs/T01_TEST_SPEC.md` describes a proposed self-owned stdio fixture. The two reference documents map hypotheses to official materials. Much of this historical design is written in Chinese.

## Status

**GATE_A=BLOCKED; GATE_B=NOT_RUN; RUNTIME_TEST=NOT_RUN.** These are publication-baseline statuses from the project's Current Status. No CLI, fixture, runner or executable security result is released here. Threats are hypotheses, not verified vulnerabilities. A design example or static consistency check cannot be counted as a runtime PASS.

The documents preserve their original protocol assumptions and reference dates. They are a research snapshot, not a current protocol conformance certification. See VALIDATION.md for publication checks. No private targets, credentials, raw logs, unpublished vulnerability disclosures or personal project records are included. Links point to public reference materials; their text is not bundled.

This publication does not change the formal roadmap or bypass either engineering gate. No additional redistribution license is granted for original design files; see RIGHTS.md. Questions and corrections are welcome in [Issues](https://github.com/laolao-dev/mcp-boundary-check/issues).
