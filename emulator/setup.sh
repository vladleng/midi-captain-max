#!/bin/bash
# Prepare the emulator for Wokwi simulation.
# Downloads CircuitPython UF2, builds an all-in-one firmware bundle,
# and copies source files for reference.
#
# Usage: ./emulator/setup.sh [--config path/to/config.json]
#
# Prerequisites: pip install pyfatfs

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
UF2_URL="https://downloads.circuitpython.org/bin/raspberry_pi_pico/en_US/adafruit-circuitpython-raspberry_pi_pico-en_US-7.3.3.uf2"
UF2_FILE="$SCRIPT_DIR/circuitpython.uf2"

echo "=== Wokwi Emulator Setup ==="
echo ""

# Download CircuitPython UF2 if not present
if [ ! -f "$UF2_FILE" ]; then
  echo "Downloading CircuitPython 7.3.3 UF2..."
  curl -L -o "$UF2_FILE" "$UF2_URL"
  echo "Done."
else
  echo "CircuitPython UF2 already downloaded."
fi
echo ""

# Build the all-in-one UF2 with firmware baked in
echo "Building firmware bundle..."
python3 "$SCRIPT_DIR/build-uf2.py" "$@"
echo ""

echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Get a Wokwi CLI token:  https://wokwi.com/dashboard/ci"
echo "  2. Export it:               export WOKWI_CLI_TOKEN=your_token"
echo "  3. Run automated tests:     ./emulator/test.sh"
echo "  4. Run interactively:       ./emulator/run.sh"
echo ""
