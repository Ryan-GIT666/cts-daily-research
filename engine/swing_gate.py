"""CTS swing-trading decision gate, PAPER ONLY. No broker SDK or network access."""
from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal
from typing import Optional
import json

@dataclass(frozen=True)
class Policy:
    max_position_twd: Decimal = Decimal("10000")
    max_portfolio_twd: Decimal = Decimal("30000")
    max_daily_loss_twd: Decimal = Decimal("500")
    min_coverage_pct: Decimal = Decimal("95")
    max_signal_age_seconds: int = 120
    min_score: int = 80
    target_gain_low_pct: Decimal = Decimal("3")
    target_gain_high_pct: Decimal = Decimal("7")
    max_holding_days: int = 21

@dataclass(frozen=True)
class Intent:
    signal_id: str
    code: str
    side: str
    shares: int
    limit_price: Decimal
    signal_at: datetime
    score: int

@dataclass(frozen=True)
class Account:
    positions: dict
    cash_twd: Decimal
    daily_realized_pnl_twd: Decimal
    pending_order_codes: tuple
    reconciled_at: datetime
    reconciled: bool = False

class Rejected(ValueError):
    pass

def check(intent: Intent, account: Account, policy: Policy, now: datetime,
          research: dict, seen_ids: set) -> dict:
    """Return a paper-order envelope, never an executable broker order."""
    def require(condition, reason):
        if not condition:
            raise Rejected(reason)
    require(now.tzinfo is not None and intent.signal_at.tzinfo is not None
            and account.reconciled_at.tzinfo is not None, "timezone_required")
    require(account.reconciled, "account_not_reconciled")
    require(0 <= (now - account.reconciled_at).total_seconds() <= 120, "stale_account")
    require(intent.signal_id and intent.signal_id not in seen_ids, "duplicate_signal")
    require(intent.side == "BUY", "buy_gate_only")
    require(intent.code.isdigit() and len(intent.code) in (4, 5), "invalid_code")
    require(isinstance(intent.shares, int) and not isinstance(intent.shares, bool)
            and intent.shares > 0, "invalid_shares")
    require(intent.limit_price.is_finite() and intent.limit_price > 0, "invalid_price")
    require(0 <= (now - intent.signal_at).total_seconds() <= policy.max_signal_age_seconds,
            "stale_signal")
    require(account.daily_realized_pnl_twd > -policy.max_daily_loss_twd, "daily_loss_limit")
    require(not account.positions and not account.pending_order_codes, "single_position_gate")
    require(account.cash_twd >= 0, "invalid_cash")
    require(research.get("schema") == "cts-public-research-v1"
            and research.get("research_only") is True and research.get("update_ok") is True,
            "invalid_research")
    require(research.get("market_data_asof") == now.date().isoformat(), "stale_research")
    universe = research.get("universe_size")
    coverage = research.get("market_coverage")
    require(type(universe) is int and type(coverage) is int and universe > 0
            and 0 <= coverage <= universe, "invalid_coverage")
    require(Decimal(coverage) * 100 / Decimal(universe) >= policy.min_coverage_pct,
            "insufficient_market_coverage")
    require(intent.score >= policy.min_score, "score_below_threshold")
    # Public research is NEVER sufficient to authorize an order.
    raise Rejected("public_research_not_tradable_requires_private_verified_signal")

def load_research(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def paper_evaluate(intent, account, policy, now, research, seen_ids):
    try:
        return {"status": "REJECTED", "reason": check(intent, account, policy, now, research, seen_ids)}
    except Rejected as exc:
        return {"status": "REJECTED", "reason": str(exc)}
