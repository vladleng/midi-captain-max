[![CI](https://github.com/MC-Music-Workshop/midi-captain-max/actions/workflows/ci.yml/badge.svg)](https://github.com/MC-Music-Workshop/midi-captain-max/actions/workflows/ci.yml)

# MIDI Captain MAX Custom Firmware

**Bidirectional, config-driven CircuitPython firmware for Paint Audio MIDI Captain foot controllers.**

## What It Does

This firmware transforms your MIDI Captain into a **bidirectional MIDI controller** where your host software (DAW, plugin host) can control the device's LEDs and display, not just receive button presses.

Momentary and toggle modes are currently supported. Many more issues are coming! See here for [all open features and issues](https://github.com/MC-Music-Workshop/midi-captain-max/issues), and [the prioritized Kanban board of upcoming work](https://github.com/orgs/MC-Music-Workshop/projects/1/views/1).

## Key Features
- 🔄 **Bidirectional MIDI** — Host can update LEDs/display state on MCM
- ⚙️ **Config-driven** — Customize button labels, CC numbers, and colors with the GUI Config Editor
- 🔄 **Dev Mode** - Quickly test config changes without rebooting
- 💾 **Custom Drive Names** - Useful when managing multiple Captains
- 🎸 **Stage-ready** — No unexpected resets, no crashes, no surprises

### Includes a **GUI Config Editor**!

<img width="1312" height="912" alt="MCM-config-editor" src="https://github.com/user-attachments/assets/5e4c0b73-074b-4895-8861-d95aea7f1426" />


## Supported Devices

| Device | Status |
|--------|--------|
| MIDI Captain STD10 | ✅ |
| MIDI Captain Mini6 | ✅  |
| MIDI Captain NANO4 | ✅  |
| ONE, DUO | pending |

# Installation

:warning: Before doing any of this, if you haven't already, please back up your existing config and firmware in a safe place for recovery or to revert to OEM firmware.

## GUI Config Editor

Download the appropriate **MIDI-Captain-MAX-Config-Editor.*** installer file from the `Assets` section below.

## Firmware

1. Download the firmware zip: midi-captain-max-latest.zip.
1. Extract the zip.
1. Connect your MIDI Captain via USB. Power it on normally.
    1. The device will mount as `CIRCUITPY` or `MIDICAPTAIN`.
    1. If the drive mounts as read-only, hold switch 1 (top-left footswitch) while plugging in USB to enable write access.
  

### macOS / Linux — deploy script (recommended)

Run the included `deploy.sh` script from the extracted zip folder:

# Quick update (preserves your existing config.json)
./deploy.sh

# First-time install — also installs required CircuitPython libraries
./deploy.sh --install

# Deploy and eject for a clean reload
./deploy.sh --eject

# Overwrite config.json with the default (resets your button mappings)
./deploy.sh --fresh
The script auto-detects your device type (STD10 or Mini6) and preserves your config.json unless you pass --fresh.

Windows — deploy script (recommended)
Run the included deploy.ps1 script from the extracted zip folder in PowerShell:

# Quick update (preserves your existing config.json)
.\deploy.ps1

# First-time install — also installs required CircuitPython libraries
.\deploy.ps1 -Install

# Deploy and eject for a clean reload
.\deploy.ps1 -Eject

# Overwrite config.json with the default (resets your button mappings)
.\deploy.ps1 -Fresh

# Specify a drive letter manually
.\deploy.ps1 -MountPoint E:\
The script auto-detects your device type (STD10 or Mini6) and preserves your config.json unless you pass -Fresh.

Manual install (any platform)
Open the extracted zip folder.
Copy all files and folders to the device drive (CIRCUITPY or MIDICAPTAIN), replacing existing files.
If you have a custom config.json with your own button mappings, keep your existing one.
First-time install on Mini6: delete config.json on the device and rename config-mini6.json to config.json.

## Configuration

### Custom USB Drive Name

If you have multiple MIDI Captain devices, you can give each one a unique name! Edit the `usb_drive_name` field in `config.json`:

```json
{
  "device": "std10",
  "usb_drive_name": "MYCAPTAIN",
  ...
}
```

**Requirements:**
- Maximum 11 characters
- Letters, numbers, and underscores only
- Will be automatically converted to uppercase

The name persists across power cycles and USB disconnects. Change it anytime by editing config.json and restarting the device.

### Config Editor App (Recommended)

The **MIDI Captain MAX Config Editor** is a desktop app that makes configuration easy!

**Download for your platform:**
- **macOS:** `MIDI-Captain-MAX-Config-Editor-[version].dmg`
- **Windows:** `MIDI-Captain-MAX-Config-Editor-[version].msi` or `MIDI-Captain-MAX-Config-Editor-[version]-setup.exe`

Get the latest release from [Releases](https://github.com/MC-Music-Workshop/midi-captain-max/releases/latest)

## Installation

### MacOS
1. Open the DMG and drag the app to your Applications folder

### Windows
1. Run the MSI installer or setup.exe
2. At this time, Windows builds are unsigned. Users will see a Windows SmartScreen warning.
3. To continue installation, click "More Info" --> "Run Anyway".
    - Signing certificates will be obtained in the near future.

## Usage

2. Launch the app and connect your MIDI Captain
3. Edit button labels, CC numbers, and colors using the visual editor
4. Save directly to the device.
5. Power cycle the device to load the new settings.

# Features

- 🖱️ **Visual editing** — No JSON syntax to learn
- ✅ **Real-time validation** — Catch errors before saving
- 🎨 **Color picker** — Visual color selection 
- 🔍 **Device detection** — Automatically detects connected MIDI Captain

## Manual Configuration

You can also edit `config.json` directly on the device:

```json
{
  "buttons": [
    {"label": "DELAY", "cc": 20, "color": [0, 0, 255]},
    {"label": "REVERB", "cc": 21, "color": [0, 255, 0]},
    {"label": "CHORUS", "cc": 22, "color": [255, 0, 255]},
    {"label": "DRIVE", "cc": 23, "color": [255, 128, 0]},
    {"label": "COMP", "cc": 24, "color": [0, 255, 255]},
    {"label": "MOD", "cc": 25, "color": [255, 255, 0]},
    {"label": "LOOP", "cc": 26, "color": [255, 0, 0]},
    {"label": "TUNER", "cc": 27, "color": [255, 255, 255]},
    {"label": "BANK-", "cc": 28, "color": [128, 128, 128]},
    {"label": "BANK+", "cc": 29, "color": [128, 128, 128]}
  ]
}
```

| Field | Description | Default |
|-------|-------------| ---------|
| `label` | Text shown on LCD (max ~6 chars) |
| `cc` | MIDI CC number sent on press (0-127) |
| `color` | RGB color for LED when ON `[R, G, B]` |
| `off_mode` | LED is `off` or `dim` when in OFF state | `off`
| `mode` | `toggle` or `momentary` button behavior | `toggle`
| `keytimes` | Number of states to cycle through (1-99) | `1`
| `states` | Array of per-state configs (for keytimes > 1) | `[]`

### Advanced: Keytimes (Multi-Press Cycling)

**Keytimes** allows a button to cycle through multiple states on repeated presses, similar to the OEM SuperMode firmware. Each state can have different MIDI values and LED colors.

#### Example: 3-State Reverb Button

```json
{
  "label": "VERB",
  "cc": 20,
  "keytimes": 3,
  "states": [
    {"cc_on": 64, "color": "blue"},      // State 1: 50% wet
    {"cc_on": 96, "color": "cyan"},      // State 2: 75% wet  
    {"cc_on": 127, "color": "white"}     // State 3: 100% wet
  ]
}
```

- **First press**: Sends CC20=64, LED shows blue
- **Second press**: Sends CC20=96, LED shows cyan
- **Third press**: Sends CC20=127, LED shows white
- **Fourth press**: Cycles back to state 1

#### Per-State Options

Each state in the `states` array can override:
- `cc_on`: MIDI CC value to send (0-127)
- `cc_off`: Value when turning off (optional)
- `color`: LED color for this state
- `label`: Display label for this state (future)

#### Notes

- Keytimes defaults to 1 (standard toggle/momentary behavior)
- Maximum 99 states per button
- Works with both toggle and momentary modes
- When cycling, the button always sends the `cc_on` value for the current state

## MIDI Protocol

### Device → Host (button presses)
| Input | MIDI Message |
|-------|--------------|
| Encoder wheel | CC 11 (0-127 position) |
| Encoder push | CC 14 (127=press, 0=release) |
| Footswitch 1-10 | CC 20-29 (127=ON, 0=OFF) |
| Expression 1 | CC 12 (0-127) |
| Expression 2 | CC 13 (0-127) |

### Host → Device (LED/state control)
Send CC to the switch on its CC Number with value 0 or 127 to set button state:
- `CC 20, value 127` → Button 1 turns ON (LED lights up)
- `CC 20, value 0` → Button 1 turns OFF (LED off/dim)

## Use Cases

- **Gig Performer / MainStage** — Sync button states with plugin bypass
- **Ableton Live** — Control track mutes/solos with visual feedback
- **Guitar Rig / Helix Native** — Effect on/off with LED confirmation
- **Any MIDI-capable host** — Generic CC control with bidirectional sync

## Repository Layout

| Path | Purpose |
|------|---------|
| `firmware/dev/` | Active firmware (copy to device) |
| `config-editor/` | Desktop config editor app (Tauri + Svelte) |
| `firmware/original_helmut/` | Helmut Keller's original code (reference) |
| `docs/` | Hardware specs, design docs |
| `tools/` | Helper scripts |

## License

Copyright © 2026 Maximilian Cascone. All rights reserved.

You may use this firmware freely for personal or commercial performances. Redistribution of modified versions requires permission. See [LICENSE](LICENSE) for details.

## Attribution

This project builds on work by **Helmut Keller** ([hfrk.de](https://hfrk.de)), whose original firmware demonstrated bidirectional MIDI on the MIDI Captain. His code is preserved in `firmware/original_helmut/` as a reference.

---

## Questions, Comments, Suggestions are welcome

[Open an issue](https://github.com/MC-Music-Workshop/midi-captain-max/issues) or check [AGENTS.md](AGENTS.md) for developer documentation.

