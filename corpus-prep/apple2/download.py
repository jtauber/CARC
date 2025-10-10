#!/usr/bin/env python3

from os import makedirs
from pathlib import Path

import requests


DSK_DIR = Path("images/dsk")


with open("errors.txt", "w") as err_file:
    for filename in open("filtered_paths.txt").readlines():
        filename = filename[2:].strip()
        # url quote the filename
        path = filename.replace("#", "%23").replace(" ", "%20")
        url = "https://www.apple.asimov.net/" + path
        print(f"Downloading {url}...")
        r = requests.get(url)
        if r.status_code == 200:
            output_path = DSK_DIR / filename
            makedirs(output_path.parent, exist_ok=True)
            with open(output_path, "wb") as out_file:
                out_file.write(r.content)
        else:
            print(f"Failed to download {url}: {r.status_code}")
            err_file.write(f"{url}\t{r.status_code}\n")
