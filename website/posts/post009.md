---
title: What is in the CATALOG of Each Disk
author: James Tauber
date: 2025-10-20
---
I decided to extract the file metadata from disks with a standard layout.

As mentioned in an earlier post: of the **12,450** disks in the initial Apple II Disk Corpus,
**7,092** appear to have a regular DOS 3.3 VTOC (based on the values at offsets `$03`, `$27`, `$34`, `$35`, `$36`, `$37`).
Of those, **6,998** have a CATALOG starting on Track `$11` Sector `$0F` and that’s what I decided to explore for this post.

There are a total of **150,558** files.

The most common file types are:

<table class="table">
  <tr><td><code>$04</code></td><td>BINARY</td><td style="text-align: right;">82,357</td></tr>
  <tr><td><code>$02</code></td><td>APPLESOFT BASIC</td><td style="text-align: right;">35,117</td></tr>
  <tr><td><code>$00</code></td><td>TEXT</td><td style="text-align: right;">26,931</td></tr>
  <tr><td><code>$01</code></td><td>INTEGER BASIC</td><td style="text-align: right;">3,138</td></tr>
  <tr><td><code>$08</code></td><td>S type</td><td style="text-align: right;">989</td></tr>
  <tr><td><code>$40</code></td><td>B type</td><td style="text-align: right;">866</td></tr>
  <tr><td><code>$10</code></td><td>RELOCATABLE</td><td style="text-align: right;">303</td></tr>
  <tr><td><code>$20</code></td><td>A type</td><td style="text-align: right;">172</td></tr>
</table>

The most common file names are:

<table class="table">
  <tr><td><code>HELLO</code>                         </td><td style="text-align: right;">4,414</td></tr>
  <tr><td><code>MENU</code>                          </td><td style="text-align: right;">785</td></tr>
  <tr><td>(7 x <code>$08</code>)                     </td><td style="text-align: right;">610</td></tr>
  <tr><td><code>BOOT0</code>                         </td><td style="text-align: right;">559</td></tr>
  <tr><td>(empty)                                    </td><td style="text-align: right;">527</td></tr>
  <tr><td><code>BOOT1</code>                         </td><td style="text-align: right;">486</td></tr>
  <tr><td><code>RWTS</code>                          </td><td style="text-align: right;">485</td></tr>
  <tr><td><code>AUTOTRACE</code>                     </td><td style="text-align: right;">470</td></tr>
  <tr><td><code>ADVANCED DEMUFFIN 1.5</code>         </td><td style="text-align: right;">442</td></tr>
  <tr><td><code>ADVANCED DEMUFFIN 1.5 DOCS</code>    </td><td style="text-align: right;">441</td></tr>
  <tr><td><code>PDP</code>                           </td><td style="text-align: right;">399</td></tr>
  <tr><td><code>SUPER DEMUFFIN</code>                </td><td style="text-align: right;">397</td></tr>
  <tr><td><code>LOGO</code>                          </td><td style="text-align: right;">385</td></tr>
  <tr><td><code>PDP.README</code>                    </td><td style="text-align: right;">275</td></tr>
  <tr><td><code>APPLESOFT</code>                     </td><td style="text-align: right;">271</td></tr>
  <tr><td><code>TITLE</code>                         </td><td style="text-align: right;">242</td></tr>
  <tr><td>(6 x <code>$08</code>)                     </td><td style="text-align: right;">231</td></tr>
  <tr><td><code>CHAIN</code>                         </td><td style="text-align: right;">195</td></tr>
  <tr><td><code>INTBASIC</code>                      </td><td style="text-align: right;">191</td></tr>
  <tr><td><code>RUNTIME</code>                       </td><td style="text-align: right;">157</td></tr>
</table>

There is undoubtedly a _lot_ of file-level deduping to do and this also demonstrates the issue of cracked disks being common in the corpus.
The `DEMUFFIN` files are, I assume, left-overs from the cracking process (in this case by the cracker “4am”). The `PDP` files might be that too.
