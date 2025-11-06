#!/usr/bin/env python3

import json
from pathlib import Path
from collections import Counter


PARENT_DIR = Path(__file__).parent.parent 

basic_files = 0
basic_disk = 0
total_disk = 0
filename_counts = Counter()

with open(PARENT_DIR / "tags.json") as f:
    tags = json.load(f)
    for disk in tags:
        if "catalog_files" in disk:
            total_disk += 1
            has_basic_files = False
            for fileentry in disk.get("catalog_files", []):
                filetype, filename, filesize = fileentry
                if filetype == 0x02:
                    has_basic_files = True
                    filename_counts[filename] += 1
                    basic_files += 1
            if has_basic_files:
                basic_disk += 1

print(f"Total disks: {total_disk}")
print(f"Disks with BASIC files: {basic_disk}")
print(f"Total BASIC files: {basic_files}")
print("Filename counts:")
for filename, count in filename_counts.most_common(20):
    print(f"  {filename}: {count}")

