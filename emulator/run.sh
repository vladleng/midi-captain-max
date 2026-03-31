#!/bin/bash
# Run MIDI Captain firmware interactively in Wokwi emulator.
# Serial output streams to your terminal; Ctrl+C to stop.
#
# Prerequisites:
#   1. Run ./emulator/setup.sh first
#   2. Set WOKWI_CLI_TOKEN env var (get from https://wokwi.com/dashboard/ci)
#
# Usage: ./emulator/run.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WOKWI_CLI="${WOKWI_CLI:-wokwi-cli}"

# Find wokwi-cli
if ! command -v "$WOKWI_CLI" &> /dev/null; then
  if [ -x "$HOME/.wokwi/bin/wokwi-cli" ]; then
    WOKWI_CLI="$HOME/.wokwi/bin/wokwi-cli"
  else
    echo "Error: wokwi-cli not found. Install: curl -L https://wokwi.com/ci/install.sh | sh"
    exit 1
  fi
fi

if [ ! -f "$SCRIPT_DIR/firmware-bundle.uf2" ]; then
  echo "Error: firmware-bundle.uf2 not found. Run ./emulator/setup.sh first."
  exit 1
fi

if [ -z "$WOKWI_CLI_TOKEN" ]; then
  echo "Error: WOKWI_CLI_TOKEN not set."
  echo "Get your token at: https://wokwi.com/dashboard/ci"
  exit 1
fi

echo "Starting Wokwi emulator (interactive)..."
echo "Press Ctrl+C to stop."
echo ""

"$WOKWI_CLI" --interactive "$SCRIPT_DIR"
