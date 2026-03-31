#!/bin/bash
# Run automated emulator tests using Wokwi CLI.
# Verifies firmware boots, detects device, and produces no errors.
#
# Prerequisites:
#   1. Run ./emulator/setup.sh first
#   2. Set WOKWI_CLI_TOKEN env var (get from https://wokwi.com/dashboard/ci)
#
# Usage: ./emulator/test.sh
#
# Exit codes:
#   0  = passed (boot banner found)
#   1  = failed (Python error detected)
#   42 = timeout (firmware didn't print expected text within 30s)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$SCRIPT_DIR/test.log"
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

echo "Running emulator tests..."
echo ""

# Run with 30s timeout
# Exit code: 0 = expect-text found, 1 = fail-text found, 42 = timeout
"$WOKWI_CLI" \
  --timeout 30000 \
  --expect-text "MIDI CAPTAIN" \
  --fail-text "Traceback" \
  --serial-log-file "$LOG_FILE" \
  --timeout-exit-code 42 \
  "$SCRIPT_DIR"

EXIT_CODE=$?

echo ""
echo "Serial log saved to: $LOG_FILE"

if [ $EXIT_CODE -eq 0 ]; then
  echo "PASSED: Firmware booted successfully."
elif [ $EXIT_CODE -eq 42 ]; then
  echo "TIMEOUT: Firmware did not print expected text within 30s."
  echo "Check $LOG_FILE for details."
  exit 1
else
  echo "FAILED: Error detected in firmware output."
  echo "Check $LOG_FILE for details."
  exit 1
fi
