"""
ONE1 Hardware Constants

Physical layout (as seen from front):
    Single switch: KEY0 (switch index 1, GP11)

LED NeoPixel chain (3 LEDs, all for the single switch):
    LEDs 0-2: KEY0

DIP switches (GP2-GP3) select the active mode/page.

Note: ONE1 has no encoder, expression pedals, or pixel-addressable display.
The 3-digit 7-segment LCD is driven via UART (GP4 TX, GP5 RX, 9600 baud)
using a proprietary frame protocol: [0xA5, seg1, seg2, seg3, 0x5A] sent 3x.
"""

import board

# NeoPixels
LED_PIN = board.GP7
LED_COUNT = 3  # 1 switch * 3 LEDs

# Footswitches - GPIO pins in index order
# Note: No encoder on ONE1, so no index 0
SWITCH_PINS = [
    board.GP11,  # 1: KEY0 (only switch)
]

# DIP switches for mode/page selection
DIP_PINS = [
    board.GP2,  # DIP 1
    board.GP3,  # DIP 2
]


def switch_to_led(switch_idx):
    """
    Convert switch index (1) to LED index (0).
    Returns None for invalid indices.

    Mapping:
        Switch 1 (KEY0) → LED 0
    """
    if switch_idx == 1:
        return 0
    return None


# No encoder on ONE1
ENCODER_A_PIN = None
ENCODER_B_PIN = None

# No expression pedals on ONE1
EXP1_PIN = None
EXP2_PIN = None
BATTERY_PIN = None

# No ST7789 pixel display on ONE1
TFT_DC_PIN = None
TFT_CS_PIN = None
TFT_SCK_PIN = None
TFT_MOSI_PIN = None

DISPLAY_WIDTH = None
DISPLAY_HEIGHT = None
DISPLAY_ROWSTART = None
DISPLAY_ROTATION = None

# Segmented LCD display (3-digit 7-segment via UART)
# Protocol: 5-byte frame [0xA5, seg1, seg2, seg3, 0x5A] at 9600 baud
# Send frame 3x with 40ms inter-frame delay
SEG_DISPLAY_TX_PIN = board.GP4
SEG_DISPLAY_RX_PIN = board.GP5
SEG_DISPLAY_BAUDRATE = 9600
SEG_DISPLAY_HEADER = 0xA5
SEG_DISPLAY_FOOTER = 0x5A
SEG_DISPLAY_DELAY_MS = 40
SEG_DISPLAY_REPEATS = 3
