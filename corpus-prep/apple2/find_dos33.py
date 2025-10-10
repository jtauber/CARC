#!/usr/bin/env python3

from pathlib import Path


DSK_DIR = Path(__file__).parent / "images" / "dsk"

total = 0
dos33_count = 0
dos33_strict_count = 0

for file in open("deduped_resize_paths.txt").readlines():
    file = file.strip()
    with open(DSK_DIR / file, "rb") as f:
        f.seek((0x11 * 0x10 + 0x00) * 0x100)  # Track 17, Sector 0
        vtoc = f.read(0x100)
        if vtoc[0x03] == 0x03 and vtoc[0x27] == 0x7A:
            dos33_count += 1
            # 23 10 00 01
            if vtoc[0x34] == 0x23 and vtoc[0x35] == 0x10 and vtoc[0x36] == 0x00 and vtoc[0x37] == 0x01:
                dos33_strict_count += 1
        total += 1

print(f"DOS 3.3 disks: {dos33_count}/{total} ({dos33_count/total:.2%})")
print(f"DOS 3.3 strict disks: {dos33_strict_count}/{total} ({dos33_strict_count/total:.2%})")

