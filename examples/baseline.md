# Independent ECC-only baseline — 2026-10-30

Production audit: **45/100, blocked for a public paid launch**, because usage accounting can lose increments, webhook delivery can reset already-spent credits, and database write failures can be acknowledged as successful. This is a qualitative triage score, not a measured security rating.

## Scope and method

Target: https://github.com/dcccrypto/ai-saas-starter at `af3d199c848a405ac221524d09e12b3adcaa0968` (shallow clone, main). README explicitly identifies a portfolio demo (README.md:10,200). Assessed hypothetical public paid launch of the existing app; actual deployment and service owners unknown.

Used only ECC `skills/production-audit/SKILL.md` from the locally fetched upstream. No FlowGuard instructions, other upstream skills, combined output, or suggested bugs were supplied to this reviewer. Read-only source review; no package installation, target execution, database, API, payment, or production access. Clean `git status --porcelain` before/after. Shallow history supplies one commit; release diff and CI history unavailable.

## Blockers

1. **High — concurrent AI generation loses usage increments (static implementation evidence).** `src/app/api/insights/route.ts:73-91,111-115` reads usage, separately calls OpenAI, then writes the previously read value plus one. Two requests can both observe usage 49/limit 50, both generate, and both write 50. The supplied migration defines ordinary integer counters (`supabase/migrations/001_initial.sql:17-18`), with no reservation/atomic consume routine. Paid-provider work occurs before persistence and charging. Remediation: atomic bounded reservation plus explicit failure/refund semantics. Concurrent runtime reproduction remains outstanding.

2. **High — replay of a signed successful-payment webhook can restore consumed allowance (static implementation evidence).** `src/app/api/billing/webhook/route.ts:94-110` unconditionally resets usage to zero on `invoice.payment_succeeded`; the handler never records/claims `event.id` (`:19-122`), and supplied schema has no processed-event table. Sequence: successful invoice → consume credits → retry same invoice event → usage zero. `checkout.session.completed` also resets usage (`:43-52`). Signature verification exists (`:19-24`) but does not make repeated delivery idempotent. Remediation: durable event/invoice deduplication with transactionally scoped reset. No real webhook was sent; deployment-side protections unknown.

3. **High — webhook database failures may receive HTTP success (static implementation evidence; SDK runtime behavior not exercised).** Database update results at `src/app/api/billing/webhook/route.ts:43-52,66-73,82-90,106-109` are awaited without checking returned `error`. If the client returns an error result rather than throws, catch is bypassed and `:122` acknowledges receipt, losing automatic retry while entitlement remains stale. `src/lib/supabase.ts:24-30,95-103` demonstrates error-result checking elsewhere. Remediation: inspect every mutation result and combine retry-safe persistence with deduplication. Confirm installed Supabase client's exact error-return behavior in an isolated test.

## High-value fixes / conditional risks

- **Billing role enforcement absent on inspected path.** Checkout (`src/app/api/billing/checkout/route.ts:10-66`) and portal (`src/app/api/billing/portal/route.ts:6-40`) require a session and current org but do not enforce owner/admin. `src/auth.ts:68-74` populates membership role; schema declares viewer/member/admin/owner (`supabase/migrations/001_initial.sql:35-43`). Whether a lower-role session is reachable through supported workflows needs validation; do not claim an observed account takeover. Define billing authority and enforce it server-side.
- `src/app/api/insights/route.ts:109-115` checks insert error but ignores usage update error, allowing a success response with uncharged usage under that failure. Cover this alongside blocker 1.

## Evidence checked

Full source: `src/app/api/insights/route.ts`, `src/app/api/insights/[id]/route.ts`, `src/app/api/billing/{checkout,portal,webhook}/route.ts`, `src/lib/{supabase,openai}.ts`, `src/auth.ts`, `src/middleware.ts`, `supabase/migrations/001_initial.sql`, `README.md`, `package.json`. Partial source: `src/lib/stripe.ts` (checkout/customer metadata and helper definitions). Repository file inventory and role/metadata reference searches, Git head/status/log.

Counterevidence: raw-body signature verification exists; insight modification filters `user_id` (`src/app/api/insights/[id]/route.ts:27-33,52-56`); checkout propagates org metadata to subscription (`src/lib/stripe.ts:140-143`). No claim that every route is unauthenticated or every webhook lacks signature validation.

## Evidence missing

No executable test script in package.json, and no test/spec paths found in inventory. This does not establish absence of external testing. No runtime, build, CI results, deployed configuration, actual database policies/functions, concurrency limits, migration rehearsal, rollback exercise, or real role provisioning examined. Provider failures and event ordering remain untested. No dependency vulnerability database consulted, so pinned versions are not labeled vulnerable.

## Next action

Implement and verify atomic credit reservation and retry-safe billing persistence in an isolated test environment before considering a public paid launch. This baseline alone does not demonstrate that a composed skill improves accuracy; compare evidence quality and coverage with the combined trial, retaining overlap and counterevidence.
