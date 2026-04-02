"""
DUO 2 Display/Bus Scanner

Scans I2C buses on common pin pairs and probes SPI display pins
to discover what kind of display the DUO uses.

Segmented LCDs are typically driven via:
  - I2C (HT16K33, TM1637, etc.)
  - SPI shift registers
  - Direct GPIO (unlikely on RP2040 with limited pins)
"""

import time
import board
import busio
import digitalio

print("=" * 50)
print("DUO 2 Display/Bus Scanner")
print("=" * 50)

# --- I2C scan on common pin pairs ---
# RP2040 I2C capable pins: any GPIO can be I2C on RP2040
# Common pairs: (SDA, SCL)
i2c_pairs = [
    (board.GP0, board.GP1),
    (board.GP2, board.GP3),
    (board.GP4, board.GP5),
    (board.GP6, board.GP7),
    (board.GP8, board.GP9),
    (board.GP10, board.GP11),
    (board.GP12, board.GP13),
    (board.GP14, board.GP15),
    (board.GP18, board.GP19),
    (board.GP20, board.GP21),
    (board.GP26, board.GP27),
]

print("\n--- I2C Bus Scan ---")
for sda, scl in i2c_pairs:
    sda_name = str(sda).split(".")[-1] if hasattr(sda, '__str__') else str(sda)
    scl_name = str(scl).split(".")[-1] if hasattr(scl, '__str__') else str(scl)
    try:
        i2c = busio.I2C(scl, sda)
        while not i2c.try_lock():
            pass
        devices = i2c.scan()
        i2c.unlock()
        i2c.deinit()
        if devices:
            print(f"  SDA={sda}, SCL={scl}: FOUND devices at {[hex(d) for d in devices]}")
        else:
            print(f"  SDA={sda}, SCL={scl}: no devices")
    except Exception as e:
        print(f"  SDA={sda}, SCL={scl}: error - {e}")

# --- Check all remaining GPIO pins for any activity ---
# Some segmented LCD controllers use custom protocols (like TM1637)
# which use CLK + DIO on any 2 GPIO pins
print("\n--- GPIO state scan (non-switch, non-NeoPixel pins) ---")
print("Reading all pins to see if any are pulled to specific states...")

test_pins = [
    ("GP0", board.GP0),
    ("GP1", board.GP1),
    ("GP2", board.GP2),
    ("GP3", board.GP3),
    ("GP4", board.GP4),
    ("GP5", board.GP5),
    ("GP6", board.GP6),
    ("GP8", board.GP8),
    ("GP10", board.GP10),
    ("GP12", board.GP12),
    ("GP13", board.GP13),
    ("GP14", board.GP14),
    ("GP15", board.GP15),
    ("GP18", board.GP18),
    ("GP19", board.GP19),
    ("GP20", board.GP20),
    ("GP21", board.GP21),
    ("GP22", board.GP22),
    ("GP23", board.GP23),
    ("GP24", board.GP24),
    ("GP25", board.LED),
    ("GP26", board.GP26),
    ("GP27", board.GP27),
    ("GP28", board.GP28),
]

for name, pin in test_pins:
    try:
        dio = digitalio.DigitalInOut(pin)
        dio.direction = digitalio.Direction.INPUT
        # Read with no pull first
        dio.pull = None
        time.sleep(0.01)
        no_pull = dio.value
        # Read with pull-up
        dio.pull = digitalio.Pull.UP
        time.sleep(0.01)
        pull_up = dio.value
        # Read with pull-down
        dio.pull = digitalio.Pull.DOWN
        time.sleep(0.01)
        pull_down = dio.value
        dio.deinit()

        # Interesting if pin is being driven externally
        # (no_pull reads a definite value, or pull-up/down don't change it)
        driven = ""
        if no_pull and not pull_down:
            driven = " << externally driven HIGH"
        elif not no_pull and pull_up:
            driven = " << externally driven LOW"
        elif no_pull == pull_up == pull_down:
            driven = " << strongly driven"

        if driven:
            print(f"  {name}: no_pull={no_pull}, up={pull_up}, down={pull_down}{driven}")
    except Exception as e:
        print(f"  {name}: error - {e}")

print("\nDone! Check for I2C devices or driven pins above.")
