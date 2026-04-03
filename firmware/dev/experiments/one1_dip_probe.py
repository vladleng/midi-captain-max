"""
ONE 1 DIP Switch Probe

Check whether the ONE has DIP switches like the DUO2 (GP0-GP3).
Read the state of candidate DIP pins and print their values.
Toggle DIP switches while watching output to confirm.
"""

import time
import board
import digitalio

# DUO2 DIP switch pins — check if ONE shares them
DIP_CANDIDATES = [
    ("GP0", board.GP0),
    ("GP1", board.GP1),
    ("GP2", board.GP2),
    ("GP3", board.GP3),
]

print("=" * 50)
print("ONE 1 DIP Switch Probe")
print("=" * 50)
print()

inputs = []
for name, pin in DIP_CANDIDATES:
    try:
        dio = digitalio.DigitalInOut(pin)
        dio.direction = digitalio.Direction.INPUT
        dio.pull = digitalio.Pull.UP
        inputs.append((name, dio))
    except Exception as e:
        print(f"  SKIP {name}: {e}")

print(f"Reading {len(inputs)} DIP candidate pins...")
print("Toggle DIP switches while watching. Ctrl+C to stop.")
print("-" * 50)

prev = {}
for name, dio in inputs:
    val = dio.value
    prev[name] = val
    state = "HIGH (off)" if val else "LOW (on)"
    print(f"  {name} = {state}")

print()

while True:
    for name, dio in inputs:
        val = dio.value
        if val != prev[name]:
            state = "HIGH (off)" if val else "LOW (on)"
            print(f"  CHANGE: {name} -> {state}")
            prev[name] = val
    time.sleep(0.05)
