# CTS | Claude Free Independent Review Packet | 2026-10-20

> Paste this entire public brief into Claude or provide this GitHub file link. Do not submit personal holdings, brokerage info, password, order number, .p12, production INI, full broker JSON, cash balance, trade cost, or personal identity.

## Role
You are an independent reviewer for CTS V5.2 swing research and PAPER_ONLY engineering. GPT is responsible for integration and Notion is the private strategy authority. Your work must not alter a live trading strategy or submit/cancel any order.

## Public inputs
1. https://github.com/Ryan-GIT666/cts-daily-research/blob/integration/cts-collab-v1/collab/START_HERE.md
2. https://github.com/Ryan-GIT666/cts-daily-research/blob/integration/cts-collab-v1/collab/STATUS.json
3. https://github.com/Ryan-GIT666/cts-daily-research/blob/integration/cts-collab-v1/collab/CTS_CYCLE_WAVE_AND_API_GATES_20261020.md
4. https://github.com/Ryan-GIT666/cts-daily-research/tree/feature/cts-swing-order-engine-v0/engine
5. https://ryan-git666.github.io/cts-daily-research/latest.json

## Verification assignment
- A. Cycle logic: Does the 1-3-week 5-15 *exchange trading days* review window accidentally become a fixed time-exit? Are S1-B/S2 and weekly-to-daily pivot decisions point-in-time, not hindsight? Explain pivot confirmation lag, ATR and performance leakage. Propose at least five deterministic test cases.
- B. Broker state gates: distinguish simulation accepted-order ACK from fill, production successful balance/inventory response from complete pending-order/fill reconciliation. Detect stale balance and missing broker quote timestamps. No actual credential access.
- C. Candidate code audit: why does test_paper_broker.py import paper_broker but engine/ contains no paper_broker.py? Note whether this is a reproducible missing module or a different supported path. Identify testing stub versus actual safe behavior.
- D. Formal-rule alignment: V5.2 is 2+1 conditional positions, but candidate swing_gate.py blocks any BUY when Account.positions is nonempty; compare without claiming the correct trade decision. Placeholder max position 10000, max daily loss 500, 95% coverage, 21-day max hold must not be mistaken for approved live policy.
- E. Research fidelity: 68 of 2168 coverage is not complete market breadth; evaluate selected-universe bias, scores at vs after asof, CI validations, time zones and fresh market-data requirements.
- F. Live readiness: enumerate negative tests for duplicate signal, partial fill, stale open orders, unknown reject, retry on timeout, service restart, request ID reuse, zero-lot quote type and fail-closed switch. Public branch must have no executable live order path.

## Required output format
Verdict: PASS_FOR_RESEARCH / NEED_FIX / BLOCKED_BY_MISSING_EVIDENCE
Scope: specific file paths, branch and SHA if available; clearly distinguish inspected vs missing sources
Findings: [P0..P3] | file/line or field | actual behavior | reproduction | risk | proposed patch or test
Regression tests: exact commands or pseudocode and expected outcomes
Cycle-model pitfalls: lookahead, overfitting, execution friction, survivorship/selection bias
Missing evidence: concise, do not request sensitive account data
Eligibility: PAPER_ONLY; BROKER_READONLY_VERIFIED does not imply LIVE_READY

Never say a free Claude web chat automatically syncs this GitHub/Notion workflow. User will manually relay a sanitized review unless a separately authorized paid API integration is implemented.