"""
DUO2 Hardware Constants

Physical layout (as seen from front):
    Top:    KEY1    (switch index 2, GP9)
    Bottom: KEY0    (switch index 1, GP11)

LED NeoPixel chain (6 LEDs, 3 per switch):
    LEDs 0-2:   KEY0 (bottom switch)
    LEDs 3-5:   KEY1 (top switch)

DIP switches (GP0-GP3) select the active mode/page.

Note: DUO2 has no encoder, expression pedals, or pixel-addressable display.
The 3-digit 7-segment LCD is driven via UART (GP4 TX, GP5 RX, 9600 baud)
using a proprietary frame protocol: [0xA5, seg1, seg2, seg3, 0x5A] sent 3x.
"""

import board

# NeoPixels
LED_PIN = board.GP7
LED_COUNT = 6  # 2 switches * 3 LEDs each

# Footswitches - GPIO pins in index order
# Note: No encoder on DUO2, so no index 0
SWITCH_PINS = [
    board.GP11,  # 1: Bottom (KEY0)
    board.GP9,   # 2: Top (KEY1)
]

# DIP switches for mode/page selection
DIP_PINS = [
    board.GP0,  # DIP 1
    board.GP1,  # DIP 2
    board.GP2,  # DIP 3
    board.GP3,  # DIP 4
]


def switch_to_led(switch_idx):
    """
    Convert switch index (1-2) to LED index (0-1).
    Returns None for invalid indices.

    Mapping:
        Switch 1 (bottom, KEY0) → LED 0
        Switch 2 (top, KEY1)    → LED 1
    """
    if 1 <= switch_idx <= 2:
        return switch_idx - 1
    return None


# No encoder on DUO2
ENCODER_A_PIN = None
ENCODER_B_PIN = None

# No expression pedals on DUO2
EXP1_PIN = None
EXP2_PIN = None
BATTERY_PIN = None

# No ST7789 pixel display on DUO2
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
