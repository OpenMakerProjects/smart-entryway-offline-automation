"""Pure local rule: monotonic seconds, warm-up and bounded motion hold."""
import math
class MotionRule:
    def __init__(self,start=0,warmup=60,hold=5):
        self.start=start;self.warmup=warmup;self.hold=hold;self.last_motion=None;self.inhibited=False;self.last_time=start
    def command(self,value):
        if value==b"STOP": self.inhibited=True;self.last_motion=None;return True
        if value==b"RESUME": self.inhibited=False;self.last_motion=None;return True
        return False
    def sample(self,now,motion):
        valid=isinstance(motion,bool) and math.isfinite(now) and now>=self.last_time
        if not valid: self.last_motion=None
        else: self.last_time=now
        ready=valid and now-self.start>=self.warmup
        if ready and motion and not self.inhibited: self.last_motion=now
        active=ready and not self.inhibited and self.last_motion is not None and now-self.last_motion<self.hold
        return {"seconds":now if math.isfinite(now) else 0,"motion":motion if isinstance(motion,bool) else None,"valid":valid,"ready":ready,"inhibited":self.inhibited,"active":active,"servo_value":0.0 if active else -1.0}
