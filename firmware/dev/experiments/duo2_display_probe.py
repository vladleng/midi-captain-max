"""
DUO 2 Display Probe

Tests the ST7789 display using the same parameters as STD10/Mini6/NANO4.
Should show colored rectangles filling the screen.

The DUO issue notes mention a "smaller screen" — if the standard 240x240
params don't work, we may need to adjust.
"""

import time
import board
import busio
import displayio
from adafruit_st7789 import ST7789

# Release any existing displays
displayio.release_displays()

# SPI setup (same pins as STD10/Mini6/NANO4)
spi = busio.SPI(clock=board.GP14, MOSI=board.GP15)
display_bus = displayio.FourWire(
    spi,
    command=board.GP12,
    chip_select=board.GP13,
    baudrate=24000000,
)

# ST7789 init (same params as other devices)
display = ST7789(
    display_bus,
    width=240,
    height=240,
    rowstart=80,
    rotation=180,
)

print("=" * 50)
print("DUO 2 Display Probe")
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

# Final: show 2 halves representing the 2 switches
print("\nShowing 2-half layout (Top=Red for KEY1, Bottom=Green for KEY0)...")

while len(group) > 0:
    group.pop()

halves = [
    (0, 0, 240, 120, 0xFF0000),      # Top half = KEY1 (top switch)
    (0, 120, 240, 120, 0x00FF00),     # Bottom half = KEY0 (bottom switch)
]

for x, y, w, h, color in halves:
    bmp = displayio.Bitmap(w, h, 1)
    pal = displayio.Palette(1)
    pal[0] = color
    tg = displayio.TileGrid(bmp, pixel_shader=pal, x=x, y=y)
    group.append(tg)

display.show(group)
print("Done! Display should show top=red, bottom=green.")

while True:
    time.sleep(1)
