"""
DUO 2 Display Test

Protocol confirmed from OEM inspection:
  - UART: GP4=TX, GP5=RX, 9600 baud
  - Frame: [0xA5, seg1, seg2, seg3, 0x5A]
  - Send frame 3 times (DP_SEND1/2/3)
  - Digit encoding: standard 7-segment, bit7 = decimal point
"""

import time
import board
import busio

HEADER = 0xA5
FOOTER = 0x5A

# Standard 7-segment digit encoding
DIGITS = [0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F]
DASH = 0x40
BLANK = 0x00

print("Starting in 5 seconds...")
time.sleep(5)

print("=" * 50)
print("DUO 2 Display Test")
print("=" * 50)

uart = busio.UART(board.GP4, board.GP5, baudrate=9600, timeout=0.1)
time.sleep(0.5)


def display_write(seg1, seg2, seg3):
    """Send display frame 3 times (matching OEM 3-phase protocol)."""
    frame = bytes([HEADER, seg1, seg2, seg3, FOOTER])
    for _ in range(3):
        uart.write(frame)
        time.sleep(0.04)  # disp_delay = 40ms


def display_number(n):
    """Display a 3-digit number (0-999)."""
    d1 = DIGITS[(n // 100) % 10] if n >= 100 else BLANK
    d2 = DIGITS[(n // 10) % 10] if n >= 10 else BLANK
    d3 = DIGITS[n % 10]
    display_write(d1, d2, d3)


# --- Test 1: Show "888" ---
print("  Showing: 888")
display_write(DIGITS[8], DIGITS[8], DIGITS[8])
time.sleep(2)

# --- Test 2: Show "123" ---
print("  Showing: 123")
display_write(DIGITS[1], DIGITS[2], DIGITS[3])
time.sleep(2)

# --- Test 3: Show "---" (dashes) ---
print("  Showing: ---")
display_write(DASH, DASH, DASH)
time.sleep(2)

# --- Test 4: All segments on ---
print("  Showing: all segments")
display_write(0x7F, 0x7F, 0x7F)
time.sleep(2)

# --- Test 5: Count 0-9 ---
print("  Counting 0-9...")
for i in range(10):
    display_write(BLANK, BLANK, DIGITS[i])
    time.sleep(0.5)

# --- Test 6: Count up ---
print("  Counting 0-999...")
for n in range(0, 1000, 7):
    display_number(n)
    time.sleep(0.05)

display_number(999)
time.sleep(2)

# --- Test 7: "Hi" ---
# H=0x76, i=0x06 (same as 1)
print("  Showing: Hi!")
display_write(0x76, 0x06, 0x00)
time.sleep(2)

print("\nDisplay test complete!")

while True:
    time.sleep(1)
