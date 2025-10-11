#!/usr/bin/env python3


from collections import Counter
from pathlib import Path


DSK_DIR = Path(__file__).parent / "images" / "dsk"

byte_counts = Counter()
row_counts = Counter()
col_counts = Counter()
for file in open("deduped_resize_paths.txt").readlines():
    file = file.strip()
    with open(DSK_DIR / file, "rb") as f:
        byte = f.read(1)
        while byte:
            byte_counts[ord(byte)] += 1
            row_counts[ord(byte) // 16] += 1
            col_counts[ord(byte) % 16] += 1
            byte = f.read(1)

ranks = {}
rank = 0
with open("byte_rank.txt", "w") as f:
    for b, count in byte_counts.most_common():
        rank += 1
        ranks[b] = rank
        f.write(f"{b:02X} {rank}\n")

col_ranks = {}
col_rank = 0
with open("column_rank.txt", "w") as f:
    for b, count in col_counts.most_common():
        col_rank += 1
        col_ranks[b] = col_rank
        f.write(f"{b:01X}_ {col_rank}\n")

row_ranks = {}
row_rank = 0
with open("row_rank.txt", "w") as f:
    for b, count in row_counts.most_common():
        row_rank += 1
        row_ranks[b] = row_rank
        f.write(f"_{b:01X} {row_rank}\n")


with open("byte_rank_heatmap.svg", "w") as f:
    f.write(
        """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 280">\n"""
    )
    for y in range(16):
        for x in range(16):
            byte = y * 16 + x
            rank = ranks[byte]
            l = (256 - rank) / 2.56
            fill = "black" if l > 30 else "#CCC"
            f.write(
                f'<rect x="{x * 16}" y="{y * 16}" width="16" height="16" fill="hsl(60, 75%, {l}%)"/>\n'
                f'<text font-family="IBM Plex Mono" x="{x * 16 + 8}" y="{y * 16 + 11}" font-size="8" text-anchor="middle" fill="{fill}">{byte:02X}</text>\n'
            )
    for z in range(16):
        col_rank = col_ranks[z]
        l = (16 - col_rank) * (100 / 16)
        fill = "black" if l > 30 else "#CCC"
        f.write(
            f'<rect x="{z * 16}" y="264" width="16" height="16" fill="hsl(60, 75%, {l}%)"/>\n'
            f'<text font-family="IBM Plex Mono" x="{z * 16 + 8}" y="275" font-size="8" text-anchor="middle" fill="{fill}">{z:01X}_</text>\n'
        )
        row_rank = row_ranks[z]
        l = (16 - row_rank) * (100 / 16)
        fill = "black" if l > 30 else "#CCC"
        f.write(
            f'<rect x="264" y="{z * 16}" width="16" height="16" fill="hsl(60, 75%, {l}%)"/>\n'
            f'<text font-family="IBM Plex Mono" x="272" y="{z * 16 + 11}" font-size="8" text-anchor="middle" fill="{fill}">_{z:01X}</text>\n'
        )
    f.write("</svg>\n")
