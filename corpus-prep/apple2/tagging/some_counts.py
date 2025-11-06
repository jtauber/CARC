#!/usr/bin/env python3

import json
from pathlib import Path
from collections import Counter


PARENT_DIR = Path(__file__).parent.parent 

total_disk = 0
vtoc_catalog_loc_count = 0
vtoc_catalog_locs = Counter()
file_count = 0
filetype_counts = Counter()
filename_counts = Counter()

with open(PARENT_DIR / "tags.json") as f:
    tags = json.load(f)
    for disk in tags:
        total_disk += 1
        if "vtoc_catalog_loc" in disk:
            vtoc_catalog_loc_count += 1
            vtoc_catalog_loc = disk["vtoc_catalog_loc"]
            vtoc_catalog_locs[vtoc_catalog_loc] += 1
            for fileentry in disk.get("catalog_files", []):
                file_count += 1
                filetype, filename, filesize = fileentry
                filetype_counts[hex(filetype)] += 1
                filename_counts[filename] += 1

print(f"Total disks: {total_disk}")
print(f"Disks with VTOC catalog loc: {vtoc_catalog_loc_count}")
print("VTOC catalog loc counts:")
for loc, count in vtoc_catalog_locs.most_common(10):
    print(f"  {loc}: {count}")
print(f"Total files: {file_count}")
print("Filetype counts:")
for filetype, count in filetype_counts.most_common(10):
    print(f"  {filetype}: {count}")
print("Filename counts:")
for filename, count in filename_counts.most_common(20):
    print(f"  {filename}: {count}")

