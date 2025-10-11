---
title: Gathering Apple II Disk Images
author: James Tauber
date: 2025-10-09
---
I want to get a lot of 6502 machine code, BASIC source, etc. so I’ve gathered a few
thousand Apple II disk images.

I started there as it’s what I'm most familiar with.

<https://www.apple.asimov.net/site_files.txt> lists **39,663** files of which **15,187** end in `.dsk` (case-insensitive).
Based on category gleaned from the file path, I identified **13,322** Apple II disk images to download.

Of these, **13,312** successfully downloaded and **13,252** are the expected size: 143,360 bytes.
Of those **13,252**, I eliminated a further **802** as having a duplicate MD5 hash.

Of the **12,450** deduplicated disk images of the right size, **7,092** (**57.0**%) of them appear to be normal DOS 3.3 disks with a regular VTOC. That’s not to say I can’t do interesting things with the other disks, but it will be a lot more difficult.

I won’t check-in all the disk images but the GitHub repo does contain the file lists and all the code I’ve written so far.
