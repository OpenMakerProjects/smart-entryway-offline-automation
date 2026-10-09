# Architecture

Local monotonic-time policy drives PIR-to-pointer behavior without cloud, internet or BLE. Hardware adapter uses gpiozero with pigpio PWM. Optional Bless/BlueZ GATT reports JSON and accepts STOP/RESUME inhibition; no direct angle command. Simulation and the legacy Controller API remain available. Cleanup rests the pointer. No process-crash watchdog is provided.
