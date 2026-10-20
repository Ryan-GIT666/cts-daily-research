import unittest
from decimal import Decimal as D
from paper_broker import PaperBroker
class PaperBrokerTests(unittest.TestCase):
    def test_buy_partial_sell(self):
        b=PaperBroker(D("10000"))
        o=b.submit("one","2313","BUY",10,D("100"))
        b.fill(o.order_id,4,D("99"))
        self.assertEqual(o.state,"PARTIAL")
        b.fill(o.order_id,6,D("100"))
        self.assertEqual(b.positions["2313"],10)
        s=b.submit("two","2313","SELL",10,D("105"))
        b.fill(s.order_id,10,D("106"))
        self.assertEqual(b.positions,{})
        self.assertEqual(b.realized_pnl,D("64"))
    def test_duplicate_submission(self):
        b=PaperBroker(D("10000"))
        a=b.submit("same","2313","BUY",10,D("100"))
        self.assertIs(a,b.submit("same","2313","BUY",10,D("100")))
        with self.assertRaisesRegex(ValueError,"idempotency_conflict"):
            b.submit("same","2313","BUY",11,D("100"))
    def test_pending_gate_and_cancel(self):
        b=PaperBroker(D("10000"))
        a=b.submit("one","2313","BUY",10,D("100"))
        with self.assertRaisesRegex(ValueError,"pending_order_exists"):
            b.submit("two","2313","BUY",10,D("100"))
        b.cancel(a.order_id)
        self.assertEqual(a.state,"CANCELED")
    def test_reject_overfill(self):
        b=PaperBroker(D("10000"))
        a=b.submit("one","2313","BUY",10,D("100"))
        with self.assertRaisesRegex(ValueError,"invalid_fill"):
            b.fill(a.order_id,11,D("99"))
    def test_no_short_selling(self):
        b=PaperBroker(D("10000"))
        with self.assertRaisesRegex(ValueError,"insufficient_position"):
            b.submit("sell","2313","SELL",1,D("100"))
if __name__=="__main__":
    unittest.main()
