# Wiring

BCM23 (physical16) receives verified3.3V PIR OUT; BCM17 (physical11) goes to3.3V-compatible servo signal. Pi GND physical6 joins sensor/servo/supply negative. Separate5V≥1A supply through1A fuse powers PIR VCC and servo V+. Pi uses its own microUSB power; do not join external positive to Pi5V pins. [Editable circuit](circuit-diagram.svg).
