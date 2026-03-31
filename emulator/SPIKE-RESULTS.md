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

### Important: Not a Local Emulator

`wokwi-cli` is **not** a local emulator — it connects to Wokwi's cloud to run the simulation. Every run consumes CI minutes from your Wokwi plan. The test script has a 30s timeout, so a single run costs ~0.5 minutes, giving roughly **100 test runs/month** on the free tier. Fine for manual testing and occasional CI, tight for per-push CI on an active branch.

### Should UF2 Bundle Be the End-User Delivery Method?

**No.** The UF2 bundle is a workaround for Wokwi's inability to inject files — it should stay emulator-only.

#### Why the gap between emulator and user delivery is narrow

CircuitPython reads `.py` files from a FAT filesystem regardless of how they got there. The emulator runs the **exact same source files** — same `code.py`, `core/`, `devices/`, etc. The only difference is how they land on the filesystem (baked into UF2 vs copied by `deploy.sh`). To keep this tight, the CI emulator build should pull from the same source tree that `deploy.sh` copies.

#### Why UF2 delivery would hurt end users

- **Kills the config editor.** The Tauri app reads/writes `config.json` directly on the mounted drive. UF2 delivery means no mounted drive, no direct file access.
- **Kills easy config editing.** Users can currently open `config.json` in any text editor.
- **Requires BOOTSEL for every update.** Users must hold a button and power-cycle instead of running `deploy.sh`.
- **Loses incremental updates.** Changing one button mapping means rebuilding and reflashing the entire UF2.
- **Loses CircuitPython's biggest advantage** — the accessible, editable filesystem.

#### What about the BOOTSEL + config-mode pattern?

Some Pico devices (running compiled C/C++ firmware) use BOOTSEL to flash a UF2 and a special keypress to enter a config-only mode that mounts a drive with just a config file. This solves a problem we don't have — we *want* the drive mounted because it's how the config editor and deploy scripts work. That pattern makes sense for compiled firmware where there's nothing useful for users to see. Ours has user-editable config and visible source files.

#### Comparison

| | Compiled C/C++ firmware | CircuitPython (our approach) |
|---|---|---|
| **Code format** | Compiled binary in UF2 | `.py` source files on FAT filesystem |
| **Install method** | BOOTSEL → copy UF2 | Mount drive → copy files |
| **Config** | Separate mechanism needed | Edit `config.json` on the drive |
| **Update** | Replace entire UF2 | Replace changed files only |
| **User access to code** | None (binary) | Full (source files visible) |

**Recommendation:** Keep file-copy delivery for users, UF2 bundle for emulator only. Address "test what you ship" by ensuring the CI build uses the same source tree as `deploy.sh`.

### Next Steps

1. **Merge the spike to main** — The approach is proven and working.

2. **Add a GitHub Actions workflow** — A CI workflow that runs `setup.sh` to build the UF2, then `test.sh` via `wokwi-cli` with a `WOKWI_CLI_TOKEN` secret. Validates firmware boots and initializes correctly on each push/PR.

3. **Build a test framework for action-outcome testing** — The current boot test is a sanity check ("did we brick it?"). Real testing requires:
   - A way to define test scenarios: input actions (button presses, encoder turns, expression pedal values) mapped to expected outcomes (MIDI messages sent, display text, LED colors)
   - Easy maintenance: adding a new button config shouldn't require rewriting test infrastructure
   - The Wokwi automation YAML (`test-boot.yaml`) is a starting point but limited and alpha-stage
   - **Open question:** Does Wokwi's serial output give enough observability to assert on MIDI output? Or do we need a test harness in the firmware itself (e.g., a test mode that logs actions to serial in a parseable format)?

### Commits on `wokwi-emulator-spike`

1. `2ca619f` — Initial scaffolding (diagram, scripts, configs)
2. `c44c350` — Working emulator with `build-uf2.py` and all fixes
