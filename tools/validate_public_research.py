#!/usr/bin/env python3
"""Read-only validation of PUBLIC CTS research. Never submits orders."""
from __future__ import annotations
import argparse
import datetime as dt
import json
from pathlib import Path
from zoneinfo import ZoneInfo

SENSITIVE = {"account", "broker_account", "account_id", "api_key", "api_secret",
             "password", "token", "credential", "holdings", "balance",
             "cash_balance", "cost_basis", "order_id", "customer_id"}
TAIPEI = ZoneInfo("Asia/Taipei")

def check(payload: object, now: dt.datetime | None = None) -> dict:
    errors, warnings = [], []
    now = now or dt.datetime.now(TAIPEI)
    if not isinstance(payload, dict):
        return {"ok": False, "trade_eligible": False, "errors": ["root must be an object"], "warnings": []}
    exposed = set()
    def walk(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if str(k).lower() in SENSITIVE:
                    exposed.add(str(k))
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)
    walk(payload)
    if exposed:
        errors.append("Sensitive fields in public JSON: " + ", ".join(sorted(exposed)))
    if payload.get("schema") != "cts-public-research-v1":
        errors.append("Unexpected or missing research schema")
    if payload.get("research_only") is not True:
        errors.append("research_only must be the boolean true")
    if payload.get("update_ok") is not True:
        warnings.append("Research upstream indicates update_ok=false")
    stamp, asof = None, None
    try:
        stamp = dt.datetime.fromisoformat(payload["generated_at"])
        if stamp.tzinfo is None:
            raise ValueError("offset required")
        asof = dt.date.fromisoformat(payload["market_data_asof"])
        if asof > stamp.astimezone(TAIPEI).date():
            errors.append("market_data_asof after publication date")
        if stamp > now + dt.timedelta(minutes=10):
            errors.append("generation timestamp from the future")
        if (now - stamp).days >= 3:
            warnings.append("Publication older than 3 days (calendar, not trading days)")
    except (KeyError, ValueError, TypeError) as exc:
        errors.append("Invalid timestamp or market date: " + str(exc))
    try:
        universe = int(payload["universe_size"])
        coverage = int(payload["market_coverage"])
        if not (universe > 0 and 0 <= coverage <= universe):
            errors.append("Invalid market coverage")
        elif coverage / universe < 0.8:
            warnings.append(f"Incomplete market coverage: {coverage}/{universe}; not market-wide")
    except (KeyError, ValueError, TypeError):
        errors.append("Missing or invalid universe/market_coverage")
        universe, coverage = 0, 0
    candidates = payload.get("candidates", [])
    if not isinstance(candidates, list):
        errors.append("candidates must be an array")
        candidates = []
    if len(candidates) > coverage:
        errors.append("Candidate count exceeds market_coverage")
    codes = set()
    for i, row in enumerate(candidates):
        if not isinstance(row, dict):
            errors.append(f"Candidate {i} not an object")
            continue
        code = str(row.get("code", ""))
        if not code.isdigit() or len(code) not in (4, 5, 6):
            errors.append(f"Invalid stock code at index {i}")
        if code in codes:
            errors.append(f"Duplicate stock code {code}")
        codes.add(code)
        try:
            if not (0 <= float(row["score"]) <= 100):
                errors.append(f"Invalid score for {code}")
        except (KeyError, ValueError, TypeError):
            errors.append(f"Missing score for {code}")
    return {"ok": not errors, "trade_eligible": False, "purpose": "PUBLIC_RESEARCH_ONLY",
            "generated_at": payload.get("generated_at"),
            "market_data_asof": payload.get("market_data_asof"),
            "universe_size": universe, "market_coverage": coverage,
            "candidate_count": len(candidates), "errors": errors, "warnings": warnings}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("input", type=Path)
    p.add_argument("--report", type=Path)
    a = p.parse_args()
    try:
        verdict = check(json.loads(a.input.read_text(encoding="utf-8")))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        verdict = {"ok": False, "trade_eligible": False, "errors": [str(exc)], "warnings": []}
    msg = json.dumps(verdict, ensure_ascii=False, indent=2)
    if a.report:
        a.report.parent.mkdir(parents=True, exist_ok=True)
        a.report.write_text(msg + "\n", encoding="utf-8")
    print(msg)
    raise SystemExit(0 if verdict["ok"] else 1)

if __name__ == "__main__":
    main()
