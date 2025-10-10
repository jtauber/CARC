`site_files.txt` comes from https://www.apple.asimov.net/site_files.txt

`filter_file_names.py` takes it and produces `filtered_paths.txt`

For now, any file path starting `./images/(demos|pd_collections|sound|programming|productivity|misc|masters|disk_utils|magazines|hardware|educational|communications|games)/` and ending in `.dsk` or `.DSK` is included.

`download.py` then downloads them all into `images/dsk`

`check_size_dupes.py` checks the file sizes and generates an MD5 hash of each file and writes a new list of non-duplicate files of size 143,360 bytes to `deduped_resize_paths.txt`
