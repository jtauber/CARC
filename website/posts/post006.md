---
title: Why So Many Sectors Start with 00 11 0X 00
author: James Tauber
date: 2025-10-11
---
As we saw in the previous post, ten out of the top 20 sector types start with `00 11 0X 00` and continue with all zeros.
I suspected why this might be the case and I’ve now confirmed the reason.

Note there are even _more_ sector types that _start_ with the sequence `00 11 0X 00` if you don’t require the rest of the sector to be zeros.

I immediately recognized the significance of `11` (decimal 17) as the track number of the catalog (i.e. directory) on Apple DOS disks and suspected the byte that followed was a sector number (it's always of the form `0X`).

Turns out almost all instances of this pattern were on other sectors on track `11`. Sector `0F` would have `00 11 0E 00`, sector `0E` would have `00 11 0D 00` and so on. This is how the disk catalog is laid out in Apple DOS 3.3, with each catalog sector pointing to the next catalog sector (usually the sector before on track `11`).

The all-zeros cases are just when that catalog sector is not needed (because there aren’t enough files). This explains why lower sector numbers came up more in the previous post (because lower catalog sectors are more likely to be empty than higher ones).

Just over half the disks in the Apple II Disk corpus seem to follow this standard DOS 3.3 catalog layout which will be crucial in working at the file rather than disk level in future explorations.
