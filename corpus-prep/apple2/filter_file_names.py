#!/usr/bin/env python3

import re


def get_paths(all_extensions=False):
    count = 0
    for line in open("site_files.txt").readlines():
        if re.match(r"\./", line):
            if re.match(r"\./MIRROR.LIST.txt$", line):
                continue
            elif re.match(r"\./site_files.txt$", line):
                continue
            elif re.match(r"\./site_index.txt$", line):
                continue
            elif re.match(r"\./documentation/", line):
                if re.match(r"\./documentation/source_code/", line):
                    continue
                elif re.match(r"\./documentation/(advertisements|apple1|apple3|applelisa|applications|os|programming|misc|games|non_english|magazines|hardware|macintosh)/", line):
                    continue
            elif re.match(r"\./emulators/", line):
                if re.match(r"\./emulators/rom_images/", line):
                    continue
                elif re.match(r"\./emulators/(kegs|mess|virtual_II|aipc|prodosemu|apple2-emu-linux|agat|bebox|lisa|apple_ii_oasis|stm|2_in_a_mac|appleIIgo|catakig|applepc|jace|mac|gus|applewin|fast_eddie|appleblossom|xgs|sara|appleibm|apple1|apple_2_for_windows|simiie|bernie|misc|appleuni|apple2000|IIe|yae|capple)/", line):
                    continue
            elif re.match(r"\./images/", line):
                if re.match(r"\./images/\.message$", line):
                    continue
                elif re.match(r"\./images/(demos|pd_collections|sound|programming|productivity|misc|masters|disk_utils|magazines|hardware|educational|communications|games)/", line):
                    if re.match(r"\./images/games/\.message$", line):
                        continue
                    if re.match(r"\./images/games/index$", line):
                        continue
                    if re.search(r"\.(dsk|DSK)$", line):
                        yield line.strip()
                        continue
                    if re.search(r"\.(woz|d13|D13|do|DO|po|PO|2mg|2MG|edd|EDD|nib|NIB)$", line):
                        if all_extensions:
                            yield line.strip()
                        continue
                    if re.search(r"\.(v2d|txt|rtf|dmg|pdf|png|zip|asm|shk|sdk|SDK|ZIP|SHK|bqy|tar|readme|bxy|BXY|TXT|sit|SIT|PDF|bad|c|docs|jpeg|img|hdv|HDV|index|tep|wav|DO_readme|bin|bsc|exec|jpg|TEXT|html|m4a|GIF|fdi|BQY|BIN|DOCS|\$E0|BNY|Z|BAS|features|ASM|rar|htm|doc|sol|gif)$", line):
                        continue
                    if re.match(r"\./images/misc/select10$", line):
                        continue
                    if re.match(r"\./images/disk_utils/saltines_super_transcopy/", line):
                        continue
                    if re.match(r"\./images/disk_utils/fatcat_docs$", line):
                        continue
                    if re.match(r"\./images/games/strategy/ssi/rings_of_zilfin/", line):
                        continue
                    if re.match(r"\./images/games/adventure/empire_of_the_overmind$", line):
                        continue
                    if re.match(r"\./images/games/action/captain_goodnight/", line):
                        continue
                    if re.match(r"\./images/games/action/who_framed_roger_rabbit/roger_rabbit_password$", line):
                        continue
                    if re.match(r"\./images/games/simulation/alert$", line):
                        continue
                    if re.match(r"\./images/games/simulation/soloflt$", line):
                        continue
                    if re.match(r"\./images/games/misc/beagle_bag_docs$", line):
                        continue
                    if re.match(r"\./images/games/collections/san_inc_dos/hero 12k file DOS \(san inc pack\).dsk \(fixes refresh bug in original game\)$", line):
                        continue
                elif re.match(r"\./images/non-english/", line):
                    continue
                elif re.match(r"\./images/(apple1|apple3|gs|applelisa|cpm)/", line):
                    continue
            elif re.match(r"\./incoming/", line):
                continue
            elif re.match(r"\./unsorted/", line):
                continue
            elif re.match(r"\./utility/", line):
                continue

        print("@@@", line)
        count += 1
        if count > 10:
            quit()


if __name__ == "__main__":
    with open("filtered_paths_all.txt", "w") as out_file:
        for path in get_paths(all_extensions=True):
            # out_file.write(path + "\n")
            out_file.write(path.split(".")[-1].upper() + "\t" + path + "\n")
