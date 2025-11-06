---
title: How the CATALOG Differs if a 4am Crack or Not
author: James Tauber
date: 2025-11-06
---
In the previous post I speculated that the counts of file names in the corpus
might be skewed due to the number of disks cracked by 4am. In this post I
separate them out.

As in the previous post, I'm just dealing with the **6,998** disks meeting
certain tests of a “normal” DOS 3.3 VTOC and CATALOG. Of those disks, **1,278**
have the string `(4am crack)` in their disk name.

The most common file names in the `(4am crack)` disk CATALOGs are:

<table class="table">
  <tr><td><code>HELLO</code>                         </td><td style="text-align: right;">1,025</td></tr>
  <tr><td><code>BOOT0</code>                         </td><td style="text-align: right;">556</td></tr>
  <tr><td><code>AUTOTRACE</code>                     </td><td style="text-align: right;">470</td></tr>
  <tr><td><code>BOOT1</code>                         </td><td style="text-align: right;">468</td></tr>
  <tr><td><code>RWTS</code>                          </td><td style="text-align: right;">459</td></tr>
  <tr><td><code>ADVANCED DEMUFFIN 1.5</code>         </td><td style="text-align: right;">439</td></tr>
  <tr><td><code>ADVANCED DEMUFFIN 1.5 DOCS</code>    </td><td style="text-align: right;">439</td></tr>
  <tr><td><code>PDP</code>                           </td><td style="text-align: right;">399</td></tr>
  <tr><td><code>SUPER DEMUFFIN</code>                </td><td style="text-align: right;">397</td></tr>
  <tr><td><code>PDP.README</code>                    </td><td style="text-align: right;">275</td></tr>
  <tr><td><code>PDP DOCS</code>                      </td><td style="text-align: right;">122</td></tr>
  <tr><td><code>MENU</code>                          </td><td style="text-align: right;">110</td></tr>
  <tr><td><code>A 4AM CRACK (README)</code>          </td><td style="text-align: right;">105</td></tr>
  <tr><td><code>TRACE2</code>                        </td><td style="text-align: right;">94</td></tr>
  <tr><td><code>TRACE</code>                         </td><td style="text-align: right;">89</td></tr>
  <tr><td><code>AUTOTRACE0</code>                    </td><td style="text-align: right;">85</td></tr>
  <tr><td><code>AUTOTRACE1</code>                    </td><td style="text-align: right;">85</td></tr>
  <tr><td><code>ADVANCED DEMUFFIN 1.1</code>         </td><td style="text-align: right;">85</td></tr>
  <tr><td><code>IOB</code>                           </td><td style="text-align: right;">66</td></tr>
  <tr><td><code>CREDITS</code>                       </td><td style="text-align: right;">53</td></tr>
</table>

However, the most common file names in the non-`(4am crack)` disk CATALOGs are:

<table class="table">
  <tr><td><code>HELLO</code>                         </td><td style="text-align: right;">3,389</td></tr>
  <tr><td><code>MENU</code>                          </td><td style="text-align: right;">675</td></tr>
  <tr><td>(7 x <code>$08</code>)                     </td><td style="text-align: right;">609</td></tr>
  <tr><td><code>(empty)                              </td><td style="text-align: right;">525</td></tr>
  <tr><td><code>LOGO</code>                          </td><td style="text-align: right;">354</td></tr>
  <tr><td><code>APPLESOFT</code>                     </td><td style="text-align: right;">237</td></tr>
  <tr><td><code>(6 x <code>$08</code>)               </td><td style="text-align: right;">231</td></tr>
  <tr><td><code>INTBASIC</code>                      </td><td style="text-align: right;">191</td></tr>
  <tr><td><code>TITLE</code>                         </td><td style="text-align: right;">191</td></tr>
  <tr><td><code>CHAIN</code>                         </td><td style="text-align: right;">179</td></tr>
  <tr><td><code>RUNTIME</code>                       </td><td style="text-align: right;">134</td></tr>
  <tr><td><code>START</code>                         </td><td style="text-align: right;">127</td></tr>
  <tr><td><code>MECC$$DISK</code>                    </td><td style="text-align: right;">123</td></tr>
  <tr><td><code>STARTUP</code>                       </td><td style="text-align: right;">121</td></tr>
  <tr><td><code>A</code>                             </td><td style="text-align: right;">116</td></tr>
  <tr><td><code>CAT</code>                           </td><td style="text-align: right;">111</td></tr>
  <tr><td><code>BOOT</code>                          </td><td style="text-align: right;">107</td></tr>
  <tr><td><code>FPBASIC</code>                       </td><td style="text-align: right;">100</td></tr>
  <tr><td><code>C</code>                             </td><td style="text-align: right;">92</td></tr>
  <tr><td><code>H</code>                             </td><td style="text-align: right;">92</td></tr>
</table>

Which seems to confirm all the files like `BOOT0`, `AUTOTRACE`, `BOOT1`, `RWTS`, `ADVANCED DEMUFFIN 1.5`,
`ADVANCED DEMUFFIN 1.5 DOCS`, `PDP`, `SUPER DEMUFFIN`, `PDP.README`, `PDP DOCS`, `A 4AM CRACK (README)`,
`TRACE2`, `TRACE`, `AUTOTRACE0`, `AUTOTRACE1`, `ADVANCED DEMUFFIN 1.1`, and possibly `IOB` and `CREDITS`
are just artifacts of the cracking process.
