import math,unittest
from src.policy import MotionRule
class MotionTests(unittest.TestCase):
 def test_warmup_and_hold(self):
  r=MotionRule();self.assertFalse(r.sample(59,True)["active"]);self.assertTrue(r.sample(60,True)["active"]);self.assertTrue(r.sample(64,False)["active"]);self.assertFalse(r.sample(65,False)["active"])
 def test_inhibit_and_resume(self):
  r=MotionRule(warmup=0);r.sample(0,True);self.assertTrue(r.command(b"STOP"));self.assertFalse(r.sample(1,True)["active"]);self.assertFalse(r.command(b"bad"));r.command(b"RESUME");self.assertFalse(r.sample(2,False)["active"]);self.assertTrue(r.sample(3,True)["active"])
 def test_invalid_and_backwards_time(self):
  r=MotionRule(warmup=0);r.sample(10,True);self.assertFalse(r.sample(11,None)["active"]);r.sample(12,True);self.assertFalse(r.sample(9,True)["valid"]);self.assertFalse(r.sample(math.nan,True)["active"])
