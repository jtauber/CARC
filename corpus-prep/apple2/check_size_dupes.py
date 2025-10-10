#!/usr/bin/env python3


from collections import defaultdict
import hashlib
from pathlib import Path


def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def analyze_files(images_dir):
    size_to_files = defaultdict(list)
    hash_to_files = defaultdict(list)
    paths = set()

    for file_path in images_dir.rglob("*"):
        if file_path.is_file():
            file_size = file_path.stat().st_size
            md5_hash = calculate_md5(file_path)
            size_to_files[file_size].append(file_path)
            hash_to_files[md5_hash].append(file_path)

            if file_size == 143_360:
                paths.add(file_path)


    total = 0
    for size, files in size_to_files.items():
        print(size, len(files), sep="\t")
        total += len(files)
    print("", total, sep="\t")

    total = 0
    for md5_hash, files in hash_to_files.items():
        if len(files) > 1:
            print(f"Duplicate files with hash {md5_hash}:")
            for file in files:
                print(f"  {file}")
            total += len(files) - 1
            for file in files[1:]:
                paths.discard(file)
            print()

    print("Total duplicate files:", total)

    print(f"Non-duplicate files with size 143360: {len(paths)}")

    with open("deduped_resize_paths.txt", "w") as out_file:
        for path in sorted(paths):
            out_file.write(f"./{path.relative_to(images_dir / "dsk")}\n")

if __name__ == "__main__":
    IMAGES_DIR = Path(__file__).parent / "images"
    analyze_files(IMAGES_DIR)
