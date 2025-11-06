#!/usr/bin/env python3

import json
from pathlib import Path


PARENT_DIR = Path(__file__).parent.parent 
DSK_DIR = PARENT_DIR / "images" / "dsk"

with open(PARENT_DIR / "tags.json") as f:
    tags = json.load(f)

for tag in tags:
    with open(DSK_DIR / tag["path"], "rb") as f:
        boot_sector = f.read(256)
        tag["boot_first_six"] = boot_sector[:6].hex().upper()

with open(PARENT_DIR / "tags.json", "w") as g:
    json.dump(tags, g, indent=2)
