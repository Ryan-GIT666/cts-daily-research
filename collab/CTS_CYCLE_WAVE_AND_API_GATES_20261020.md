# CTS V5.2 | 1-3 Week Swing Cycle & Broker API Gates | 2026-10-20

> PUBLIC / SANITIZED SPECIFICATION ONLY. No real positions, balances, account info, order IDs, API keys, secret, credentials, certificate or broker payloads belong here.
> This is an implementation addendum. Formal strategy authority remains private Notion CTS V5.2. PAPER_ONLY and AUTO_LIVE=DISABLED.

## Verified vs not verified
- Confirmed on user's private Windows machine: ESUN SDK 2.2.0 simulation order response succeeded with accepted-order code and order identifier (ACK is not proof of fill).
- Confirmed on user's private Windows machine: production read-only login, balance and inventory calls returned data twice. No live orders submitted.
- NOT confirmed: production pending orders / fills / cancellation / reconnect / partial fills / idempotency / zero-lot real-time quotes / actual fees.
- Collaboration: Public Research Contract GitHub Actions has at least two completed success runs; this is public JSON contract validation, not strategy or live trading validation.
- Historical public research: 2026-10-20 asof, 68 evaluated of 2168 symbol universe (~3.14%). Never treat scores as a marketwide executable ranking.

## Cycle thesis (research, not executable order)
1. Cycle backdrop: weekly/daily observed pivots L->H and H->L, half-wave duration distributions; annotate observation vs confirmed pivot timestamp; no lookahead.
2. Setup stage: Market Regime Gate then S0/S1-A/S1-B/S2/S3. S1-B requires real bottoming evidence and invalidation; S2 may qualify without waiting for exact low; S3 is extended/low remaining R:R.
3. Horizon: target 1-3 weeks (~5-15 exchange trading days); target net 3-7% is a hypothesis, not fixed take-profit, time-based auto-liquidation, or guaranteed result.
4. Review landmarks counted from actually filled trade date: day 0-2 support/invalidation; 3-5 impulse/volume; 6-10 first resistance vs conditional extension and net R:R; 11-15 profit protection/rotation; >15 force REASSESS, not automatic sell. Event and risk break override any schedule.
5. Volatility adaptation only as CANDIDATE until backtested: ATR relative to price, swing duration percentile, relative strength and industry event, MFE/MAE distributions, transaction cost and liquidity. Insufficient data -> CYCLE_UNCERTAIN, not a buy recommendation.
6. Prioritize confirmed existing holdings risk over open new positions. Standard V5.2 2+1 portfolio structure remains authority; a candidate code gate blocking every existing position is not a replacement policy.

## Data hierarchy and privacy contract
- Private Notion Skill = strategy authority; private position subpage = verified broker inventory and confirmed fills; intraday analysis = asof/timestamps and scenario; Stock Pool = candidates.
- Windows only = SDK credentials, broker data, positions, cash, fills, pending orders, risk gate and execution. Preserve credentials in local secrets; no full logs on public repositories.
- GitHub gh-pages/latest.json = research_only=true public candidate subset; it must never mutate private holdings, grant trading, or claim full coverage.
- GPT = orchestrate research and structured evidence, code review and regression; no independent broker authority.
- Claude Free = manually initiated second reviewer of sanitized public docs/diff with P0-P3 issues, not a linked service or automatic trader.

## Verification gates
| Gate | Evidence needed | Current |
|---|---|---|
| PUBLIC_DATA_GATE | current exchange day, asof, coverage, missing symbols and timezone | Contract CI passed; coverage limited |
| SIM_ORDER_ACK | broker sandbox response code and order ID, no live endpoint | VERIFIED |
| BROKER_READONLY | production read-only account calls with valid data timestamps | VERIFIED for inventory/balance; 2nd balance not latest |
| BROKER_RECONCILED | inventory + pending orders + fills + reserved buying power reconciled | NOT VERIFIED |
| CYCLE_BACKTEST | point-in-time entry, fees, slippage, spread, unfilled orders, cross-regime, out-of-sample | NOT VERIFIED |
| SHADOW_20D | >=20 trading days forward paper signals vs observed broker/market conditions | NOT VERIFIED |
| LIVE_MANUAL | explicit per-order human approval, tested cancellation/status/idempotency and kill switch | DISABLED |
| AUTO_LIVE | independent explicit approval and per-day/position circuit breakers | DISABLED |

## Specific known candidate discrepancies to fix
- Branch feature/cts-swing-order-engine-v0 lists engine/test_paper_broker.py but engine/paper_broker.py is absent; tests cannot all be declared passed until dependency is provided and rerun.
- engine/swing_gate.py uses placeholder position/day-loss/coverage thresholds and a 21-day hold default: NOT formal V5.2 limits. Clarify 21 calendar days vs 5-15 trading day review before any promotion.
- Public research scores cannot become private validated signals simply by increasing universe coverage. Fail closed.
- All project work stays on an isolated branch; do not change production broker settings or gh-pages research publication as part of review.

## Runbook by cadence
- 08:35: update date gate, market regime, candidate research and missing-data flags (study only).
- During trading: local-only read-only positions/pending-orders/quote source; trigger HOLD/REVIEW/RISK_ALERT and human-approved draft; do not execute orders.
- 13:15: save last actionable scenario and overnight plan to private Notion.
- 16:45: publish **sanitized research-only** JSON if data contract passes and local publishing schedule actually ran; failing refresh must not be disguised as fresh.
- Weekly: audit candidate transition durations, holding day age, cycle prediction vs outcome, missed moves, and OOS/shadow evidence.

## References
- Private strategy: https://app.notion.com/p/3c943d9c613e8127aa28f3b0c9818bc1
- Public research: https://ryan-git666.github.io/cts-daily-research/latest.json
- Collaboration status: collab/STATUS.json
- Claude checklist: collab/CLAUDE_CYCLE_REVIEW_20261020.md