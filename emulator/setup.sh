#!/bin/bash
# Prepare the emulator directory for Wokwi simulation.
# Copies firmware source files into the emulator directory so Wokwi
# can load them into the simulated Pico's flash filesystem.
#
# Usage: ./emulator/setup.sh [config-file]
#   config-file: optional path to a config JSON (default: firmware/dev/config.json)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
FIRMWARE_DIR="$PROJECT_ROOT/firmware/dev"
CONFIG_FILE="${1:-$FIRMWARE_DIR/config.json}"

echo "=== Wokwi Emulator Setup ==="
echo ""

# Validate config file
if [ ! -f "$CONFIG_FILE" ]; then
  echo "Error: Config file not found: $CONFIG_FILE"
  exit 1
fi

# Copy firmware source files into emulator directory
# Wokwi loads all files in the project directory into the Pico's flash filesystem
echo "Copying firmware files..."
cp "$FIRMWARE_DIR/code.py" "$SCRIPT_DIR/code.py"
cp "$FIRMWARE_DIR/boot.py" "$SCRIPT_DIR/boot.py"
cp "$CONFIG_FILE" "$SCRIPT_DIR/config.json"

# Copy core/ and devices/ modules
rm -rf "$SCRIPT_DIR/core" "$SCRIPT_DIR/devices"
cp -r "$FIRMWARE_DIR/core" "$SCRIPT_DIR/core"
cp -r "$FIRMWARE_DIR/devices" "$SCRIPT_DIR/devices"

echo "Done."
echo ""
echo "Files copied to: $SCRIPT_DIR"
echo "Config used:     $CONFIG_FILE"
echo ""
echo "Next steps:"
echo "  1. Get a Wokwi CLI token:  https://wokwi.com/dashboard/ci"
echo "  2. Export it:               export WOKWI_CLI_TOKEN=your_token"
echo "  3. Run the emulator:        ./emulator/run.sh"
echo "  4. Run automated tests:     ./emulator/test.sh"
echo ""
