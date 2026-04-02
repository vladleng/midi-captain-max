"""
DUO 2 OEM Module Inspector

Import the OEM module, let it init the display (shows "51.1"),
then when user presses Ctrl+C, dump the module's internals.
"""

import sys
import time

print("=" * 50)
print("DUO 2 OEM Inspector")
print("=" * 50)
print()
print("Importing OEM module... display should show '51.1'")
print("Once display is showing, press Ctrl+C to inspect.")
print()

try:
    import midicaptain2s
except KeyboardInterrupt:
    print("\n--- Interrupted! Inspecting module... ---\n")

m = sys.modules.get("midicaptain2s")
if not m:
    print("Module not in sys.modules!")
else:
    attrs = dir(m)
    print("Module attributes: %s\n" % attrs)

    for name in ["uart", "uart2", "display_buf", "digits_hex",
                  "hex_pc", "hex_cc", "hex_nt", "hex_NA",
                  "hex_dot", "hex_HID", "hex_VER",
                  "disp_delay", "dp_state", "disp_flag",
                  "disp_numb", "disp_clear",
                  "DP_IDLE", "DP_SEND1"]:
        if hasattr(m, name):
            val = getattr(m, name)
            print("  %s = %s" % (name, repr(val)))

    # Try to get UART baudrate
    if hasattr(m, "uart"):
        u = m.uart
        print("\n  uart type: %s" % type(u))
        if hasattr(u, "baudrate"):
            print("  uart.baudrate = %s" % u.baudrate)
        print("  uart dir: %s" % dir(u))

    if hasattr(m, "uart2"):
        u2 = m.uart2
        print("\n  uart2 type: %s" % type(u2))
        if hasattr(u2, "baudrate"):
            print("  uart2.baudrate = %s" % u2.baudrate)

print("\nDone!")

while True:
    time.sleep(1)
