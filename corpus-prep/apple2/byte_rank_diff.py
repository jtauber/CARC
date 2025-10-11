#!/usr/bin/env python3


from collections import Counter
from pathlib import Path


DSK_DIR = Path(__file__).parent / "images" / "dsk"

byte_counts = Counter()
row_counts = Counter()
col_counts = Counter()
for file in ["./images/games/rpg/ultima/ultima_IV/u4boot.dsk"]:
    file = file.strip()
    with open(DSK_DIR / file, "rb") as f:
        byte = f.read(1)
        while byte:
            byte_counts[ord(byte)] += 1
            row_counts[ord(byte) // 16] += 1
            col_counts[ord(byte) % 16] += 1
            byte = f.read(1)

a_ranks = {}
rank = 0
for b, count in byte_counts.most_common():
    rank += 1
    a_ranks[f"{b:02X}"] = rank

a_col_ranks = {}
col_rank = 0
for b, count in col_counts.most_common():
    col_rank += 1
    a_col_ranks[f"{b:01X}_"] = col_rank

a_row_ranks = {}
row_rank = 0
for b, count in row_counts.most_common():
    row_rank += 1
    a_row_ranks[f"_{b:01X}"] = row_rank

b_ranks = {}
for line in open("byte_rank.txt"):
    b, rank = line.strip().split()
    b_ranks[b] = int(rank)

b_col_ranks = {}
for line in open("column_rank.txt"):
    b, rank = line.strip().split()
    b_col_ranks[b] = int(rank)

b_row_ranks = {}
for line in open("row_rank.txt"):
    b, rank = line.strip().split()
    b_row_ranks[b] = int(rank)


with open("byte_rank_diff.svg", "w") as f:
    f.write(
        """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 280">\n"""
    )
    for y in range(16):
        for x in range(16):
            b = y * 16 + x
            rank_diff = a_ranks[f"{b:02X}"] - b_ranks[f"{b:02X}"]
            if rank_diff > 0:
                color = f"hsl(120, {rank_diff / 2.56}%, {100 - rank_diff / 2.56}%)"
            else:
                color = f"hsl(0, {-rank_diff / 2.56}%, {100 + rank_diff / 2.56}%)"
            fill = "black" if (100 - abs(rank_diff) / 2.56) > 50 else "#EEE"
            f.write(
                f'<rect x="{x * 16}" y="{y * 16}" width="16" height="16" fill="{color}"/>\n'
                f'<text font-family="IBM Plex Mono" x="{x * 16 + 8}" y="{y * 16 + 11}" font-size="8" text-anchor="middle" fill="{fill}">{b:02X}</text>\n'
            )
    for z in range(16):
        rank_diff = a_col_ranks[f"{z:01X}_"] - b_col_ranks[f"{z:01X}_"]
        if rank_diff > 0:
            color = f"hsl(120, {rank_diff / 0.16}%, {100 - rank_diff / 0.16}%)"
        else:
            color = f"hsl(0, {-rank_diff / 0.16}%, {100 + rank_diff / 0.16}%)"
        fill = "black" if (100 - abs(rank_diff) / 0.16) > 50 else "#EEE"
        f.write(
            f'<rect x="{z * 16}" y="264" width="16" height="16" fill="{color}"/>\n'
            f'<text font-family="IBM Plex Mono" x="{z * 16 + 8}" y="275" font-size="8" text-anchor="middle" fill="{fill}">{z:01X}_</text>\n'
        )
        rank_diff = a_row_ranks[f"_{z:01X}"] - b_row_ranks[f"_{z:01X}"]
        if rank_diff > 0:
            color = f"hsl(120, {rank_diff / 0.16}%, {100 - rank_diff / 0.16}%)"
        else:
            color = f"hsl(0, {-rank_diff / 0.16}%, {100 + rank_diff / 0.16}%)"
        fill = "black" if (100 - abs(rank_diff) / 0.16) > 50 else "#EEE"
        f.write(
            f'<rect x="264" y="{z * 16}" width="16" height="16" fill="{color}"/>\n'
            f'<text font-family="IBM Plex Mono" x="272" y="{z * 16 + 11}" font-size="8" text-anchor="middle" fill="{fill}">_{z:01X}</text>\n'
        )
    f.write("</svg>\n")
