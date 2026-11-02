# Forward test observations

FlowGuard was usable in this Codex session: three cached dependencies were verified, no dependency fetching occurred, source-only investigation produced a validated report, and missing native Trail of Bits execution was represented as fallback rather than a completed run.

Observed usability/validation limitations:

1. `doctor.available=true` means pinned checkout availability, not native workflow executability. The adapter prose makes the difference clear; machine consumers must not treat it as native capability readiness. Future doctor output could expose host capability separately.
2. The evidence contract is intentionally extensible, but the current validator only checks that frontier/adapters/coverage/gaps are arrays, not that their records contain the documented fields. A report could validate while omitting the actual frontier rationale or gap owners. Strengthening required nested fields would improve reviewability.
3. Snapshot catches file content changes but omits symlinks and empty directories. It cannot prove a fully unchanged filesystem or enforce read-only access. The trial uses source hash and Git status checks plus policy boundaries, not isolation.
4. Native ToB workflow was not exercised and no upstream per-function fan-out was reproduced. The integration claim should remain instruction-guided/fallback in this environment.
5. Sequential baseline and combined trial share reviewer and knowledge; improvements are not an independent efficacy benchmark. The auth identity hypothesis in combined.md must stay a hypothesis until framework internals and isolated sign-in behavior are checked.

No target executable, package installer, database, production or provider endpoint was accessed. `review.json` validated with the helper. Before/after snapshot equality is recorded in snapshot-check.json.

## Corrections after forward test

Doctor now reports runtime=not-probed separately. Validator now requires documented nested record keys and nonempty frontier/coverage, with negative tests. Snapshot records file and directory symlinks without following them; empty directories and transient writes remain outside its coverage. The 39-file target had no such links, so existing before/after evidence remains comparable.
