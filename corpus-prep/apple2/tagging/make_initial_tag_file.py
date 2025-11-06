#!/usr/bin/env python3

import json
from pathlib import Path


PARENT_DIR = Path(__file__).parent.parent 
DSK_DIR = PARENT_DIR / "images" / "dsk"

tags = []

for path_string in open(PARENT_DIR / "deduped_resize_paths.txt"):
    tags.append({
        "path": path_string.strip(),
    })

with open(PARENT_DIR / "tags.json", "w") as g:
    json.dump(tags, g, indent=2)

