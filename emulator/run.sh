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

if [ ! -f "$SCRIPT_DIR/code.py" ]; then
  echo "Error: code.py not found. Run ./emulator/setup.sh first."
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

wokwi-cli --interactive "$SCRIPT_DIR"
