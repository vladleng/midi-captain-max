## What Just Happened

This was a spike to find a working emulator for testing MIDI Captain firmware without a physical device. Here's the journey:

### The Problem

PR 33 (from Copilot) tried to use `rp2040js-circuitpython` but the CLI flags it assumed (`--image`, `--fs`) **don't exist** in that tool. We closed it.

### Evaluating Wokwi

You suggested Wokwi. Research showed it had promising CI support via `wokwi-cli`, so we went for it.

### Three Walls We Hit

1. **`wokwi-cli` requires a `firmware` field** in `wokwi.toml` — even for CircuitPython projects. Setting `firmware = ""` or `firmware = "code.py"` both failed.

2. **File injection is browser-only.** The Wokwi browser editor copies project files into the simulated Pico's flash. The CLI does not — it just uploads the UF2 and runs it. So providing the CircuitPython UF2 booted CP fine, but it ran the default "Hello World" `code.py` baked into the UF2, not our firmware.

3. **CircuitPython's filesystem is read-only from serial.** We tried using `mpremote` over RFC2217 serial forwarding to upload files after boot. CircuitPython refused: `Cannot remount '/' when visible via USB.` The only way to get write access is via `boot.py` — which we can't modify because we can't write to the filesystem. Chicken-and-egg.

### The Solution: All-in-One UF2

The breakthrough: **bake our firmware files directly into the UF2's FAT filesystem.**

CircuitPython on the Pico uses a FAT12 filesystem in the last 1MB of flash (offset `0x10100000`). The `build-uf2.py` script:

1. Creates a 1MB FAT12 image using `pyfatfs` (pure Python — no OS tools)
2. Populates it with `code.py`, `boot.py`, `config.json`, `core/`, `devices/`, `lib/`, `fonts/`
3. Converts the FAT image to UF2 format at the correct flash address
4. Concatenates it with the CircuitPython 7.3.3 firmware UF2
5. Outputs `firmware-bundle.uf2` — a single file containing everything

### What's on the Branch

```
emulator/
├── build-uf2.py          # Builds the all-in-one UF2 (the key piece)
├── setup.sh              # Downloads CP UF2, runs build-uf2.py
├── test.sh               # Runs wokwi-cli with --expect-text/--fail-text
├── run.sh                # Interactive mode
├── wokwi.toml            # Points firmware at firmware-bundle.uf2
├── diagram.json          # STD10 hardware: 8 buttons, 1 NeoPixel
├── test-boot.yaml        # Wokwi automation scenario (button presses)
├── requirements.txt      # Adafruit libs (for future use)
└── configs/
    ├── test-std10.json   # Correct schema, 10 buttons + encoder + expression
    └── test-mini6.json   # Correct schema, 6 buttons
```

### What Works

When you run `./emulator/test.sh`, the firmware:
- Boots CircuitPython 7.3.3
- Loads our `code.py` from the embedded filesystem
- Detects STD10 device from `config.json`
- Loads all 10 button configs, encoder, expression pedals
- Initializes display (fonts load from embedded filesystem)
- Initializes 11 switches and MIDI
- Enters the main loop and sends MIDI CC messages

### Known Limitations

- **GP23/24/25 not available** in Wokwi's Pico model (internal pins) — 3 of 10 buttons can't be wired in the diagram. The firmware still runs fine; those switches just float.
- **50 free CI minutes/month** on Wokwi — enough for weekly runs, tight for per-push
- **Automation scenarios are alpha** — button press simulation via YAML works but isn't battle-tested
- **Requires `WOKWI_CLI_TOKEN`** — needs a secret for CI

### Two Commits on `wokwi-emulator-spike`

1. `2ca619f` — Initial scaffolding (diagram, scripts, configs)
2. `c44c350` — Working emulator with `build-uf2.py` and all fixes
