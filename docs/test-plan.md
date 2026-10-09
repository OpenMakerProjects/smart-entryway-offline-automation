# Test plan

Cloud tests cover 60s warmup,5s hold, inhibition/resume, invalid/backward time, compatibility Controller API and BLE schema/status encoding. CI installs Linux dependencies, compiles Python, runs deterministic CLI and artifacts. Hardware/PIR/pigpio/BlueZ/BLE tests not performed. First power the sensor only, verify OUT≤3.3V; fit a loose pointer with no load, calibrate pulse endpoints, then test motion and STOP after warmup.
