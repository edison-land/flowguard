# FlowGuard combined read-only trial

**Advisory No-go** for a provisional public paid launch of dcccrypto/ai-saas-starter, commit `af3d199c848a405ac221524d09e12b3adcaa0968`. The code identifies itself as a portfolio demo; this does not judge any actual deployment. Owner: **unassigned**. Date: 2026-10-30. No approval or target mutation performed.

## What actually ran

FlowGuard instructions, adapter contract and evidence contract were read. `doctor work/upstream` verified three pinned source checkouts. ECC was applied as instruction-guided risk analysis with dynamically chosen paths. Production Excellence entry, AGENTS, evidence/gate/handoff references and the production-readiness and verification-methodology sibling entries were explicitly loaded. Other specialist methods were not executed; operational evidence is gapped.

Trail of Bits' native workflow was **unavailable** in this host. Its entry and format/domain resources were read to assess the adapter, but its native Workflow runtime and registered function agent were not invoked. The context notes below are independent FlowGuard fallback analysis, not an assertion of running or porting the upstream skill. No copying of upstream prose, workflow runtime, installer hooks or target scripts.

## Independent context notes: identity and shared state

- OAuth signIn calls `upsertUser` but discards its returned local user (`src/auth.ts:26-37`). The helper creates/returns a database UUID user and current organization (`src/lib/supabase.ts:129-170`, `supabase/migrations/001_initial.sql:24-32`). JWT callback preserves email, and session callback copies `token.sub` to `session.user.id` (`src/auth.ts:44-77`). API handlers use that identity to query the local UUID column (`src/app/api/insights/route.ts:63-70`). The equality between framework subject and local UUID is not established by inspected source. Framework internals are unavailable, so this remains a hypothesis, not a reproduced login defect.
- AI generation and invoice processing share `organizations.ai_credits_used`. API generation reads/checks, performs paid external work, then writes a previously read value plus one (`src/app/api/insights/route.ts:73-115`, `src/lib/openai.ts:48-62`). Invoice delivery separately resets the same value (`src/app/api/billing/webhook/route.ts:94-110`). A cross-request allowance invariant needs atomic reservations and period/event identity; neither is established in the supplied path/schema.
- Signature checking and user-id filters are real counterevidence: webhook verification at `src/app/api/billing/webhook/route.ts:19-24`; insight modification scoped by user at `src/app/api/insights/[id]/route.ts:27-33,52-56`. They do not prove credit atomicity, identity mapping or event idempotency.

## Findings and verification boundary

The machine-readable [review.json](review.json) binds each source location to a file hash and includes triggers, effects, counterevidence, confidence and remedies.

| ID | Mechanism | Status | Priority |
| --- | --- | --- | --- |
| FG-01 | Framework JWT subject not mapped to locally generated database user ID | Hypothesis; installed auth behavior not tested | High; could block core flows |
| FG-02 | Separate read/check/write allows lost usage increments | Source-observed; runtime concurrency not executed | High |
| FG-03 | Successful invoice replay resets already-consumed usage | Source-observed; no event replay executed | High |
| FG-04 | Webhook may acknowledge returned database errors | Hypothesis; exact SDK failure contract not executed | High |

If FG-01 prevents valid-user API access, FG-02 is a latent risk after identity correction rather than proof of a currently reachable exploit. This dependency must be retained when planning tests.

## Cross-domain packet and handoff

Risk class provisionally High: customer-facing auth and billing. Source review supplies business flow and risk mechanisms, not a complete production-readiness packet. Migration/recovery rehearsal, capacity/cost model, incident history, launch ownership/release approval and integration/QA results remain explicit gaps in review.json. New service status, absent incidents and external safeguards cannot be inferred from missing repository files. No owner or deadline invented.

Handoff: proposed launch held until operator establishes ownership and evidence boundary, identity mapping is verified, bounded credit consumption and retry-safe entitlement persistence are demonstrated in isolation. No waiver, sign-off, review cadence or escalation body supplied. Native upstream gates conflict on whether a Low-risk owner can self-approve an exception; irrelevant here (High risk, no exception sought), and never used to bypass FlowGuard's human-waiver rule.

## Comparison with ECC-only baseline

Baseline independently used ECC before this combined pass and found credit race, payment reset replay, unchecked write errors and conditional billing role authorization. The combined follow-up added a concrete cross-function identity hypothesis and made the dependency between that hypothesis and credit-path reachability explicit. It also adds source hashes, adapter execution modes, a dynamic question frontier and accountable evidence gaps. Both runs recommend blocking a paid launch; no claim that composition changed the verdict or that ECC alone could not find the identity issue.

This is one sequential, non-blinded follow-up by the same reviewer, with extra reading time. It demonstrates workflow artifacts and a plausible coverage benefit, **not causal accuracy improvement**. Repeat independent equal-budget trials on multiple repositories, include negative controls, and confirm SDK-dependent hypotheses before claiming effectiveness.
