#!/usr/bin/env python3

import json
from pathlib import Path


PARENT_DIR = Path(__file__).parent.parent 
DSK_DIR = PARENT_DIR / "images" / "dsk"

with open(PARENT_DIR / "tags.json") as f:
    tags = json.load(f)

for tag in tags:
    if tag.get("vtoc_catalog_loc") == "110F":
        with open(DSK_DIR / tag["path"], "rb") as f:
            files = []
            sector = 15
            while sector > 0:
                f.seek((0x11 * 0x10 + sector) * 0x100)  # Track 17, Sector sector
                catalog = f.read(0x100)
                for i in range(0x0B, 0xFF, 0x23):
                    buff = catalog[i:i+0x23]
                    if buff[0x00] == 0x00:
                        continue
                    if buff[0x00] == 0xFF:  # deleted
                        continue
                    file_type = buff[0x02] & 0x7F
                    file_name = repr("".join(chr(int(buff[j]) & 0x7F) for j in range(0x03, 0x21)))[1:-1]
                    file_length = buff[0x21] + (buff[0x22] << 8)
                    files.append((file_type, file_name, file_length))
                tag["catalog_files"] = files
                if catalog[0x01] != 0x11:
                    break
                if catalog[0x02] != sector - 1:
                    break
                sector -= 1


with open(PARENT_DIR / "tags.json", "w") as g:
    json.dump(tags, g, indent=2)
