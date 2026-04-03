"""
ONE 1 NeoPixel Probe

Lights up LEDs one at a time on GP7 to find the exact count.
Watch the device and note:
  1. How many LEDs light up total
  2. Which LED index corresponds to the switch position
  3. When it stops (pixels beyond the chain stay dark)

Tries up to 6 pixels (DUO2 count) to be safe.
ONE has 1 switch, expecting 3 LEDs.
"""

import time
import board
import neopixel

LED_PIN = board.GP7
MAX_TEST = 6  # Try up to this many

print("=" * 50)
print("ONE 1 NeoPixel Probe")
print("=" * 50)

pixels = neopixel.NeoPixel(LED_PIN, MAX_TEST, brightness=0.3, auto_write=True)
pixels.fill((0, 0, 0))
time.sleep(1)

print(f"\nLighting LEDs one at a time (0 to {MAX_TEST - 1})...")
print("Watch the device. Note which LEDs light up.\n")

for i in range(MAX_TEST):
    pixels.fill((0, 0, 0))
    pixels[i] = (255, 0, 0)  # Red
    print(f"  LED {i} = RED")
    time.sleep(1.0)

pixels.fill((0, 0, 0))
print("\nDone. Now lighting groups of 3 (per-switch clusters)...")
time.sleep(1)

colors = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
]

# Light groups of 3 in different colors
for group in range(2):
    start = group * 3
    pixels.fill((0, 0, 0))
    color = colors[group]
    for j in range(3):
        if start + j < MAX_TEST:
            pixels[start + j] = color
    print(f"  Group {group}: LEDs {start}-{start+2} = {color}")
    time.sleep(2.0)

pixels.fill((0, 0, 0))
print("\nAll off. Report what you saw!")
