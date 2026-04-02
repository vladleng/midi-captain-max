"""
NANO4 Hardware Constants

Physical layout (as seen from front):
    Top row:    TL    TR    (switch indices 1-2)
    Bottom row: BL    BR    (switch indices 3-4)

LED NeoPixel chain (12 LEDs, 3 per switch):
    LEDs 0-1:   Top row (TL, TR)
    LEDs 2-3:   Bottom row (BL, BR)

Note: NANO4 has no encoder or expression pedal inputs.
All switch pins are a subset of STD10/Mini6 pins.
"""

import board

# NeoPixels
LED_PIN = board.GP7
LED_COUNT = 12  # 4 switches * 3 LEDs each

# Footswitches - GPIO pins in index order
# Note: No encoder on NANO4, so no index 0
SWITCH_PINS = [
    board.GP1,   # 1: Top-left (TL)
    board.LED,   # 2: Top-right (TR) - repurposed LED pin (GP25)
    board.GP9,   # 3: Bottom-left (BL)
    board.GP10,  # 4: Bottom-right (BR)
]


def switch_to_led(switch_idx):
    """
    Convert switch index (1-4) to LED index (0-3).
    Returns None for invalid indices.

    Mapping:
        Switch 1-2 (top row)    → LED 0-1
        Switch 3-4 (bottom row) → LED 2-3
    """
    if 1 <= switch_idx <= 4:
        return switch_idx - 1
    return None


# No encoder on NANO4
ENCODER_A_PIN = None
ENCODER_B_PIN = None

# No expression pedals on NANO4
EXP1_PIN = None
EXP2_PIN = None
BATTERY_PIN = None

# Display (ST7789 over SPI) - same as STD10/Mini6
TFT_DC_PIN = board.GP12
TFT_CS_PIN = board.GP13
TFT_SCK_PIN = board.GP14
TFT_MOSI_PIN = board.GP15

# ST7789 parameters - same as STD10/Mini6
DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 240
DISPLAY_ROWSTART = 80
DISPLAY_ROTATION = 180
