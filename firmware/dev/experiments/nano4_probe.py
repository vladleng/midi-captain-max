"""
NANO 4 Hardware Probe Script

Deploy as code.py on the NANO 4 to discover switch pin mappings.
Connect via serial console (screen /dev/tty.usbmodem* 115200) and
press each footswitch one at a time. The script prints which GPIO
pins changed state.

Based on the approach used for Mini6 reverse engineering.
"""

import time
import board
import digitalio

# All usable GPIO pins on RP2040 / Pico
# Excludes SPI display pins (GP12-15) and NeoPixel (GP7) and UART (GP16-17)
# to avoid conflicts with known hardware.
ALL_PINS = [
    ("GP0", board.GP0),
    ("GP1", board.GP1),
    ("GP2", board.GP2),
    ("GP3", board.GP3),
    ("GP4", board.GP4),
    ("GP5", board.GP5),
    ("GP6", board.GP6),
    # GP7 = NeoPixel (skip)
    ("GP8", board.GP8),
    ("GP9", board.GP9),
    ("GP10", board.GP10),
    ("GP11", board.GP11),
    # GP12-15 = SPI display (skip)
    # GP16-17 = UART MIDI (skip)
    ("GP18", board.GP18),
    ("GP19", board.GP19),
    ("GP20", board.GP20),
    ("GP21", board.GP21),
    ("GP22", board.GP22),
    ("GP23", board.GP23),
    ("GP24", board.GP24),
    ("GP25", board.LED),       # board.LED = GP25
    ("GP26", board.GP26),
    ("GP27", board.GP27),
    ("GP28", board.GP28),
    ("VBUS_SENSE", board.VBUS_SENSE),
]

print("=" * 50)
print("NANO 4 Pin Scanner")
print("=" * 50)
print()
print("Setting up all pins as INPUT with PULL_UP...")
print("Press footswitches one at a time.")
print("Pins that go LOW on press will be reported.")
print()

# Set up all pins
inputs = []
for name, pin in ALL_PINS:
    try:
        dio = digitalio.DigitalInOut(pin)
        dio.direction = digitalio.Direction.INPUT
        dio.pull = digitalio.Pull.UP
        inputs.append((name, dio))
    except Exception as e:
        print(f"  SKIP {name}: {e}")

print(f"Monitoring {len(inputs)} pins. Press switches now...\n")

# Read baseline (all should be HIGH with pull-up, no switch pressed)
time.sleep(0.5)
baseline = {}
for name, dio in inputs:
    baseline[name] = dio.value

print("Baseline (all pins, True=HIGH):")
for name, val in baseline.items():
    if not val:
        print(f"  ** {name} = {val} (already LOW at baseline!)")
print()
print("Watching for changes... (Ctrl+C to stop)")
print("-" * 50)

# Track which pins are currently pressed to avoid repeat prints
pressed = set()

while True:
    for name, dio in inputs:
        val = dio.value
        was_high = baseline[name]

        if was_high and not val and name not in pressed:
            # Pin went LOW = switch pressed
            print(f"  PRESS detected on: {name}")
            pressed.add(name)
        elif val and name in pressed:
            # Pin went back HIGH = switch released
            print(f"  release: {name}")
            pressed.discard(name)

    time.sleep(0.02)  # 20ms debounce/poll
