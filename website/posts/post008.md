---
title: Where the Variations in the DOS 3.3 Boot Sector Happen
author: James Tauber
date: 2025-10-12
---
Following on from the previous post,
I started wondering where the different DOS-3.3-style boot sector types diverge so I
constructed the following visualization.

This is just a stacked bar chart with the x-axis representing the number of bytes into the sector
and the bars showing the proportion of disks with identical bytes up until that point.

The brightest bars (at the bottom of the stack) represent the normal DOS 3.3 boot sector and so sudden drops indicate a larger number of disks that diverge from that point.
The biggest drops are labeled with the offset at which they occur.

<img src="/CARC/figures/boot_sector.svg">

In a normal DOS 3.3 boot sector, the code runs from `01` to `4C`, bytes `4D` to `5C` contain a table of data (mapping logical sectors to physical sectors), bytes `5D` to `FC` aren’t directly used by the boot process but can be used for DOS patches, and bytes `FD` to `FF` are some more data.

The fact a drop happens after `4A` rather than after `4C` suggests the final `JMP` has been changed. I’ll explore the variations in more detail in future posts.
