# USB Drive Disable: Boot Ordering Constraint

## Background

The original `boot.py` used a simple `if/else` to gate the USB drive on Switch 1:

```python
if enable_usb_drive:
    print("🔓 USB DRIVE ENABLED")
    # Leave USB enabled (default CircuitPython behavior)
else:
    storage.disable_usb_drive()
    print("🔒 USB drive disabled")
```

This worked because the `if` branch never called any storage API — it just left
CircuitPython's default USB-enabled state in place.

## What Changed

The custom drive name feature (`usb_drive_name`) requires calling
`storage.remount("/", readonly=False, label=usb_drive_name)` to apply the label.
This call **initializes the USB mass storage subsystem**, which introduces an
ordering constraint: `storage.disable_usb_drive()` must be called **before** any
USB initialization occurs. If `remount()` runs first (even in a different code
path in the same boot.py execution), `disable_usb_drive()` may silently fail in
some CircuitPython versions.

## The Pattern

To satisfy this constraint, `boot.py` now uses two separate `if` blocks instead
of `if/else`:

```python
# STEP 1: Disable USB if needed (must come first)
if not enable_usb_drive:
    storage.disable_usb_drive()
    print("🔒 USB drive disabled")

# STEP 2: Configure USB if enabled (only runs after disable check)
if enable_usb_drive:
    storage.remount("/", readonly=False, label=usb_drive_name)
    print(f"🔓 USB DRIVE ENABLED as '{usb_drive_name}'")
```

Since only one condition can be true, the runtime behavior is equivalent to
`if/else`. But this structure guarantees that `disable_usb_drive()` appears
**before** `remount()` in the source, which is the safer pattern — it makes the
ordering obvious and avoids any risk of future refactors accidentally reversing
the calls.

## CircuitPython USB Timing

When CircuitPython boots:

1. `boot.py` runs first (before USB enumeration)
2. During `boot.py`, code decides USB configuration via storage APIs
3. After `boot.py` completes, USB enumeration occurs
4. **Key rule:** `disable_usb_drive()` must run before any call that touches
   USB (including `remount()`)

## Testing

**Test 1: USB Disabled (performance mode, default)**
1. Power on device **without** holding Switch 1
2. **Expected:** No USB drive appears on computer
3. Serial console: "🔒 USB drive disabled (hold switch 1 during boot to enable)"

**Test 2: USB Enabled (update mode)**
1. Hold Switch 1 while powering on
2. **Expected:** USB drive appears with custom name (e.g., "MIDICAPTAIN")
3. Serial console: "🔓 USB DRIVE ENABLED as 'MIDICAPTAIN'"

**Test 3: Toggle behavior**
1. Power on without Switch 1 → no drive
2. Power off
3. Power on WITH Switch 1 → drive appears
4. Power off
5. Power on without Switch 1 → no drive again

## Related Documentation

- [Custom USB drive names](custom-drive-names.md)
- CircuitPython storage module: https://docs.circuitpython.org/en/latest/shared-bindings/storage/
- MIDI Captain boot behavior: [hardware-reference.md](hardware-reference.md)
