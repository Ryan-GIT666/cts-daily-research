import unittest
from datetime import datetime, timezone
from decimal import Decimal
from swing_gate import Policy, Intent, Account, paper_evaluate

NOW = datetime(2026, 10, 20, 9, 10, tzinfo=timezone.utc)
class GateTests(unittest.TestCase):
    def setUp(self):
        self.intent = Intent("test-1", "2313", "BUY", 10, Decimal("100"), NOW, 90)
        self.account = Account({}, Decimal("10000"), Decimal("0"), (), NOW, True)
        self.research = {"schema":"cts-public-research-v1","research_only":True,"update_ok":True,
                         "market_data_asof":NOW.date().isoformat(),"universe_size":2168,
                         "market_coverage":68}
    def evaluate(self):
        return paper_evaluate(self.intent, self.account, Policy(), NOW, self.research, set())
    def test_actual_public_coverage_blocks(self):
        self.assertEqual(self.evaluate()["reason"], "insufficient_market_coverage")
    def test_even_full_coverage_not_trade_authority(self):
        self.research["market_coverage"] = 2168
        self.assertEqual(self.evaluate()["reason"],
                         "public_research_not_tradable_requires_private_verified_signal")
    def test_duplicate_signal_blocks(self):
        self.assertEqual(paper_evaluate(self.intent,self.account,Policy(),NOW,self.research,
                                        {"test-1"})["reason"], "duplicate_signal")
    def test_position_blocks(self):
        self.account = Account({"2313":10}, Decimal("10000"), Decimal("0"), (), NOW, True)
        self.assertEqual(self.evaluate()["reason"], "single_position_gate")
    def test_stale_account_blocks(self):
        self.account = Account({}, Decimal("10000"), Decimal("0"), (), NOW, False)
        self.assertEqual(self.evaluate()["reason"], "account_not_reconciled")
    def test_invalid_price_blocks(self):
        self.intent = Intent("test-1","2313","BUY",10,Decimal("NaN"),NOW,90)
        self.assertEqual(self.evaluate()["reason"], "invalid_price")
    def test_loss_limit_blocks(self):
        self.account = Account({},Decimal("10000"),Decimal("-500"),(),NOW,True)
        self.assertEqual(self.evaluate()["reason"], "daily_loss_limit")
    def test_sell_is_not_implemented(self):
        self.intent = Intent("test-1","2313","SELL",10,Decimal("100"),NOW,90)
        self.assertEqual(self.evaluate()["reason"], "buy_gate_only")
if __name__ == "__main__":
    unittest.main()
