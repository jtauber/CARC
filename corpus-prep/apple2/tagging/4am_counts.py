#!/usr/bin/env python3

import json
from pathlib import Path
from collections import Counter


PARENT_DIR = Path(__file__).parent.parent 

total_disk = 0
total_disk_4am = 0
filetype_counts_non = Counter()
filetype_counts_4am = Counter()
filename_counts_non = Counter()
filename_counts_4am = Counter()

with open(PARENT_DIR / "tags.json") as f:
    tags = json.load(f)
    for disk in tags:
        if "catalog_files" in disk:
            total_disk += 1
            if "(4am crack)" in disk["path"]:
                total_disk_4am += 1
            for fileentry in disk.get("catalog_files", []):
                filetype, filename, filesize = fileentry
                if "(4am crack)" in disk["path"]:
                    filetype_counts_4am[hex(filetype)] += 1
                    filename_counts_4am[filename] += 1
                else:
                    filetype_counts_non[hex(filetype)] += 1
                    filename_counts_non[filename] += 1

print(f"Total disks: {total_disk}")
print(f"Total (4am crack) disks: {total_disk_4am}")
print("Filetype counts (not 4am crack):")
for filetype, count in filetype_counts_non.most_common(10):
    print(f"  {filetype}: {count}")
print("Filetype counts (4am crack):")
for filetype, count in filetype_counts_4am.most_common(10):
    print(f"  {filetype}: {count}")
print("Filename counts (not 4am crack):")
for filename, count in filename_counts_non.most_common(20):
    print(f"  {filename}: {count}")
print("Filename counts (4am crack):")
for filename, count in filename_counts_4am.most_common(20):
    print(f"  {filename}: {count}")

