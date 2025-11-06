#!/usr/bin/env python3

import json
from pathlib import Path


PARENT_DIR = Path(__file__).parent.parent 
DSK_DIR = PARENT_DIR / "images" / "dsk"

with open(PARENT_DIR / "tags.json") as f:
    tags = json.load(f)

for tag in tags:
    with open(DSK_DIR / tag["path"], "rb") as f:
        f.seek((0x11 * 0x10 + 0x00) * 0x100)  # Track 17, Sector 0
        vtoc = f.read(0x100)
        if vtoc[0x03] == 0x03 and vtoc[0x27] == 0x7A:
            tag["vtoc_03_27"] = True
            if vtoc[0x34] == 0x23 and vtoc[0x35] == 0x10 and vtoc[0x36] == 0x00 and vtoc[0x37] == 0x01:
                tag["vtoc_34_35_36_37"] = True
                tag["vtoc_volume_number"] = vtoc[0x06:0x07].hex().upper()
                tag["vtoc_catalog_loc"] = vtoc[0x01:0x03].hex().upper()



with open(PARENT_DIR / "tags.json", "w") as g:
    json.dump(tags, g, indent=2)
