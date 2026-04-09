${NOTES}

# First: Backup!

**Before doing any of this, if you haven't already, please back up your existing config and firmware in a safe place** for recovery or to revert to OEM firmware:

1. Mount the device to your computer. You may have to hold down Button 1/0 to force it to mount.
2. Copy all of the content to a safe place on your computer.

# Installation

Download  [MIDI-Captain-MAX-${VERSION}-complete.zip](https://github.com/MC-Music-Workshop/midi-captain-max/releases/download/${VERSION}/MIDI-Captain-MAX-${VERSION}-complete.zip) from the `Assets` section below.

## GUI Config Editor

The "complete" package contains installers for Mac and Windows. Use the appropriate installer for your OS.

## MIDI Captain Firmware

1. Connect your MIDI Captain via USB and power it on.
    - The device will mount as `CIRCUITPY` or `MIDICAPTAIN`.
    - If the drive mounts as read-only, hold switch 1 (top-left footswitch) while plugging in USB to enable write access.
1. Extract the firmware.zip in the downloaded "complete" package.

Note: The scripts auto-detect your device type (STD10, Mini6, NANO4, DUO2, or ONE) and preserve your `config.json` unless you pass `--fresh / -Fresh` (Mac/Win)

### macOS / Linux

Run the included `deploy.sh` script from the extracted zip folder:

```bash
# Quick update (preserves your existing config.json)
./deploy.sh

# First-time install — also installs required CircuitPython libraries
./deploy.sh --install

# Deploy and eject for a clean reload
./deploy.sh --eject

# Overwrite config.json with the default - resets your button mappings
./deploy.sh --fresh

# Deploy to a device with a custom drive name, see Custom Drive Names below
./deploy.sh /Volumes/<device-name> # Mac
./deploy.sh /path/to/mount # Linux
```

### Windows

Run the included `deploy.ps1` script from the extracted zip folder in PowerShell:

```powershell
# Quick update (preserves your existing config.json)
.\deploy.ps1

# First-time install — also installs required CircuitPython libraries
.\deploy.ps1 -Install

# Deploy and eject for a clean reload
.\deploy.ps1 -Eject

# Overwrite config.json with the default (resets your button mappings)
.\deploy.ps1 -Fresh

# Specify a drive letter manually, see Custom Drive Names below
.\deploy.ps1 -MountPoint E:\
```

### Custom Drive Names

If you've renamed your device's USB drive (via the `usb_drive_name` setting in `config.json`), specify the mount point manually:

- **macOS**: `./deploy.sh /Volumes/<your-drive-name>`
- **Linux**: `./deploy.sh /media/$USER/<your-drive-name>`
- **Windows**: `.\deploy.ps1 -MountPoint E:\`

### Manual install (any platform)

1. Open the extracted zip folder.
1. Copy all files and folders to the device drive (`CIRCUITPY` or `MIDICAPTAIN`), replacing existing files.
    - If you have a custom `config.json` with your own button mappings, keep your existing one.
1. **First-time install on non-STD10:** delete `config.json` on the device and rename `config-<deviceType>.json` to `config.json`.

---

Eject and reconnect the device to reload the firmware. If anything goes wrong, it's fully recoverable: mount the device, erase the contents, and copy your backed-up files back.
