#!/usr/bin/env python3

import json
from pathlib import Path
from collections import Counter, defaultdict

from a2disk import handle
from applesoft import Detokenize


PARENT_DIR = Path(__file__).parent.parent 
DSK_DIR = PARENT_DIR / "images" / "dsk"

seen_hash_before = set()

count = 0
tokens = Counter()
token_disks = defaultdict(set)
token_files = defaultdict(set)

with open(PARENT_DIR / "tags.json") as f:
    tags = json.load(f)
    for disk in tags:
        if "catalog_files" in disk:
            for fileentry in disk.get("catalog_files", []):
                filetype, filename, filesize = fileentry
                if filetype == 0x02:
                    f = DSK_DIR / disk["path"]
                    try:
                        h = handle(f, filename)
                        m = h.get_md5()
                        if m not in seen_hash_before:
                            count += 1
                            seen_hash_before.add(m)
                            for token_id, token_label in Detokenize(h.data).tokens():
                                tokens[(token_id, token_label)] += 1
                                token_disks[(token_id, token_label)].add(disk["path"])
                                token_files[(token_id, token_label)].add((disk["path"], filename))
                    except:
                        m = "ERROR"


print("Unique BASIC files by content:", count)

print("Most common tokens:")
for (token_id, token_label), count in tokens.most_common():
    print(f'  <tr><td><code>${token_id:02X}</code></td><td><code>{token_label}</code></td><td style="text-align: right;">{count:,}</td><td style="text-align: right;">{len(token_files[(token_id, token_label)]):,}</td><td style="text-align: right;">{len(token_disks[(token_id, token_label)]):,}</td></tr>')
