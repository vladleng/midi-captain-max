"""
DUO 2 DIP Switch Probe

Monitors GP0-GP3 (suspected DIP switch pins) and GP5 (unknown).
Flip each DIP switch one at a time and note which pin changes.

Also monitors for any changes that might reveal display-related pins.
"""

import time
import board
import digitalio

PROBE_PINS = [
    ("GP0", board.GP0),
    ("GP1", board.GP1),
    ("GP2", board.GP2),
    ("GP3", board.GP3),
    ("GP5", board.GP5),
]

print("=" * 50)
print("DUO 2 DIP Switch Probe")
print("=" * 50)
print()

inputs = []
for name, pin in PROBE_PINS:
    dio = digitalio.DigitalInOut(pin)
    dio.direction = digitalio.Direction.INPUT
    dio.pull = digitalio.Pull.UP
    inputs.append((name, dio))

# Read initial state
time.sleep(0.2)
prev = {}
for name, dio in inputs:
    prev[name] = dio.value
    state = "HIGH" if dio.value else "LOW"
    print(f"  {name} = {state}")

print()
print("Flip DIP switches one at a time. Changes will be reported.")
print("-" * 50)

while True:
    for name, dio in inputs:
        val = dio.value
        if val != prev[name]:
            state = "HIGH" if val else "LOW"
            print(f"  {name} changed to {state}")
            prev[name] = val
    time.sleep(0.02)
