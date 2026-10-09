"""Explicit hardware adapter; BCM numbering, pigpio PWM and guaranteed cleanup."""
import asyncio,json,time
from .policy import MotionRule
async def operate(iterations,interval,enable_ble):
    from gpiozero import Servo,DigitalInputDevice
    from gpiozero.pins.pigpio import PiGPIOFactory
    factory=PiGPIOFactory(host="localhost")
    servo=None;pir=None;server=None
    rule=MotionRule(start=time.monotonic())
    try:
        servo=Servo(17,initial_value=-1,min_pulse_width=0.001,max_pulse_width=0.002,frame_width=0.02,pin_factory=factory)
        pir=DigitalInputDevice(23,pull_up=False,pin_factory=factory)
        if enable_ble:
            from .ble import start
            server=await start(rule,asyncio.get_running_loop())
        step=0
        while iterations<=0 or step<iterations:
            record=rule.sample(time.monotonic(),bool(pir.value))
            servo.value=record["servo_value"]
            print(json.dumps({"project_id":16,"mode":"hardware",**record},sort_keys=True),flush=True)
            if server:
                from .ble import publish
                publish(server,record)
            step+=1;await asyncio.sleep(interval)
    finally:
        if servo:servo.min();servo.close()
        if pir:pir.close()
        if server:await server.stop()
        factory.close()
