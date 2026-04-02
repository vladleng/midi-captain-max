"""
NANO 4 Display Probe

Tests the ST7789 display using the same parameters as STD10/Mini6.
Should show colored rectangles filling the screen.
"""

import time
import board
import busio
import displayio
from adafruit_st7789 import ST7789

# Release any existing displays
displayio.release_displays()

# SPI setup (same pins as STD10/Mini6)
spi = busio.SPI(clock=board.GP14, MOSI=board.GP15)
display_bus = displayio.FourWire(
    spi,
    command=board.GP12,
    chip_select=board.GP13,
    baudrate=24000000,
)

# ST7789 init (same params as STD10/Mini6)
display = ST7789(
    display_bus,
    width=240,
    height=240,
    rowstart=80,
    rotation=180,
)

print("=" * 50)
print("NANO 4 Display Probe")
print("=" * 50)

# Create a simple color fill test
group = displayio.Group()

colors = [
    (0xFF0000, "RED"),
    (0x00FF00, "GREEN"),
    (0x0000FF, "BLUE"),
    (0xFFFFFF, "WHITE"),
]

for hex_color, name in colors:
    bitmap = displayio.Bitmap(240, 240, 1)
    palette = displayio.Palette(1)
    palette[0] = hex_color
    bg = displayio.TileGrid(bitmap, pixel_shader=palette, x=0, y=0)

    while len(group) > 0:
        group.pop()
    group.append(bg)
    display.show(group)

    print(f"  Showing: {name}")
    time.sleep(1.5)

# Final: show 4 colored quadrants representing the 4 switches
print("\nShowing 4-quadrant layout (TL=Red, TR=Green, BL=Blue, BR=Yellow)...")

while len(group) > 0:
    group.pop()

quadrants = [
    (0, 0, 120, 120, 0xFF0000),      # TL = Red
    (120, 0, 120, 120, 0x00FF00),     # TR = Green
    (0, 120, 120, 120, 0x0000FF),     # BL = Blue
    (120, 120, 120, 120, 0xFFFF00),   # BR = Yellow
]

for x, y, w, h, color in quadrants:
    bmp = displayio.Bitmap(w, h, 1)
    pal = displayio.Palette(1)
    pal[0] = color
    tg = displayio.TileGrid(bmp, pixel_shader=pal, x=x, y=y)
    group.append(tg)

display.show(group)
print("Done! Display should show 4 colored quadrants.")

while True:
    time.sleep(1)
