#!/usr/bin/env python3
"""Build an all-in-one UF2 containing CircuitPython firmware + CIRCUITPY filesystem.

Creates a UF2 that includes both the CircuitPython runtime and a FAT filesystem
with our firmware files (code.py, boot.py, config.json, core/, devices/, lib/).
This UF2 can be used with wokwi-cli for emulator testing.

Usage:
  python3 emulator/build-uf2.py [--config path/to/config.json]

Requires:
  pip install pyfatfs
"""

import argparse
import io
import os
import struct
import sys

from pyfatfs.PyFat import PyFat
from pyfatfs.PyFatFS import PyFatFS

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
FIRMWARE_DIR = os.path.join(PROJECT_ROOT, "firmware", "dev")

CP_UF2 = os.path.join(SCRIPT_DIR, "circuitpython.uf2")
OUTPUT_UF2 = os.path.join(SCRIPT_DIR, "firmware-bundle.uf2")

# CircuitPython filesystem layout for Pico (2MB flash)
FS_FLASH_START = 0x10100000
FS_SIZE = 1024 * 1024  # 1MB

# UF2 constants
UF2_MAGIC0 = 0x0A324655
UF2_MAGIC1 = 0x9E5D5157
UF2_FINAL_MAGIC = 0x0AB16F30
UF2_FLAG_FAMILY = 0x00002000
RP2040_FAMILY_ID = 0xE48BFF56
UF2_DATA_SIZE = 256  # bytes of flash data per UF2 block


def create_fat_image(config_path):
  """Create a FAT12 filesystem image with firmware files using pyfatfs."""
  img_path = os.path.join(SCRIPT_DIR, "circuitpy.img")

  # Create empty image file, then format as FAT12
  with open(img_path, "wb") as f:
    f.truncate(FS_SIZE)
  pf = PyFat()
  pf.mkfs(img_path, fat_type=PyFat.FAT_TYPE_FAT12, size=FS_SIZE, label="CIRCUITPY")
  pf.close()

  # Open with pyfatfs and populate
  fs = PyFatFS(filename=img_path)

  def add_file(local_path, fs_path):
    """Add a single file to the FAT filesystem."""
    with open(local_path, "rb") as src:
      content = src.read()
    with fs.open(fs_path, "wb") as dest:
      dest.write(content)

  def add_directory(local_dir, fs_dir):
    """Recursively add a directory to the FAT filesystem."""
    fs.makedir(fs_dir)
    for entry in sorted(os.listdir(local_dir)):
      local_path = os.path.join(local_dir, entry)
      fs_path = f"{fs_dir}/{entry}"
      if os.path.isdir(local_path):
        add_directory(local_path, fs_path)
      else:
        add_file(local_path, fs_path)

  # Add firmware files
  add_file(os.path.join(FIRMWARE_DIR, "code.py"), "/code.py")
  add_file(os.path.join(FIRMWARE_DIR, "boot.py"), "/boot.py")
  add_file(config_path, "/config.json")

  # Add source directories
  for dirname in ["core", "devices", "lib", "fonts"]:
    src = os.path.join(FIRMWARE_DIR, dirname)
    if os.path.exists(src):
      add_directory(src, f"/{dirname}")

  fs.close()
  print(f"  Copied firmware files to filesystem image")
  return img_path


def binary_to_uf2(data, base_address):
  """Convert raw binary data to UF2 format."""
  num_blocks = (len(data) + UF2_DATA_SIZE - 1) // UF2_DATA_SIZE
  uf2_data = bytearray()

  for i in range(num_blocks):
    offset = i * UF2_DATA_SIZE
    chunk = data[offset:offset + UF2_DATA_SIZE]
    # Pad to UF2_DATA_SIZE if needed
    chunk = chunk + b"\x00" * (UF2_DATA_SIZE - len(chunk))

    # Build UF2 block (512 bytes)
    block = struct.pack(
      "<IIIIIIII",
      UF2_MAGIC0,
      UF2_MAGIC1,
      UF2_FLAG_FAMILY,
      base_address + offset,
      UF2_DATA_SIZE,
      i,
      num_blocks,
      RP2040_FAMILY_ID,
    )
    block += chunk
    # Pad to 476 bytes of data area
    block += b"\x00" * (476 - len(chunk))
    block += struct.pack("<I", UF2_FINAL_MAGIC)

    uf2_data.extend(block)

  return bytes(uf2_data)


def build_bundle(config_path):
  """Build the all-in-one UF2."""
  if not os.path.exists(CP_UF2):
    print(f"Error: CircuitPython UF2 not found at {CP_UF2}")
    print("Run: curl -L -o emulator/circuitpython.uf2 https://downloads.circuitpython.org/bin/raspberry_pi_pico/en_US/adafruit-circuitpython-raspberry_pi_pico-en_US-7.3.3.uf2")
    sys.exit(1)

  print("Building all-in-one UF2...")

  # Step 1: Create FAT filesystem image
  print("1. Creating CIRCUITPY filesystem image...")
  img_path = create_fat_image(config_path)
  print(f"   Image: {img_path} ({os.path.getsize(img_path)} bytes)")

  # Step 2: Read the filesystem image
  with open(img_path, "rb") as f:
    fs_data = f.read()

  # Ensure it's exactly FS_SIZE
  if len(fs_data) > FS_SIZE:
    print(f"Error: Filesystem image too large ({len(fs_data)} > {FS_SIZE})")
    sys.exit(1)
  fs_data = fs_data + b"\xFF" * (FS_SIZE - len(fs_data))

  # Step 3: Convert filesystem to UF2
  print("2. Converting filesystem to UF2 format...")
  fs_uf2 = binary_to_uf2(fs_data, FS_FLASH_START)

  # Step 4: Read the CircuitPython firmware UF2
  with open(CP_UF2, "rb") as f:
    cp_uf2 = f.read()

  # Step 5: Concatenate: firmware UF2 + filesystem UF2
  print("3. Concatenating firmware + filesystem...")
  # Need to fix block numbers in both halves
  cp_blocks = len(cp_uf2) // 512
  fs_blocks = len(fs_uf2) // 512
  total_blocks = cp_blocks + fs_blocks

  # Rewrite block numbers in firmware UF2
  combined = bytearray()
  for i in range(cp_blocks):
    block = bytearray(cp_uf2[i * 512:(i + 1) * 512])
    struct.pack_into("<II", block, 20, i, total_blocks)  # blockno, numblocks
    combined.extend(block)

  # Rewrite block numbers in filesystem UF2
  for i in range(fs_blocks):
    block = bytearray(fs_uf2[i * 512:(i + 1) * 512])
    struct.pack_into("<II", block, 20, cp_blocks + i, total_blocks)
    combined.extend(block)

  # Step 6: Write output
  with open(OUTPUT_UF2, "wb") as f:
    f.write(combined)

  print(f"4. Done! Output: {OUTPUT_UF2}")
  print(f"   Firmware blocks: {cp_blocks}")
  print(f"   Filesystem blocks: {fs_blocks}")
  print(f"   Total size: {len(combined)} bytes ({len(combined) / 1024:.0f} KB)")

  # Clean up
  if os.path.exists(img_path):
    os.remove(img_path)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Build all-in-one CircuitPython + firmware UF2")
  parser.add_argument(
    "--config",
    default=os.path.join(FIRMWARE_DIR, "config.json"),
    help="Path to config.json (default: firmware/dev/config.json)",
  )
  args = parser.parse_args()

  if not os.path.exists(args.config):
    print(f"Error: Config file not found: {args.config}")
    sys.exit(1)

  build_bundle(args.config)
