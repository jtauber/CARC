---
title: Apple Disk Controller ROM
---

The disk hardware is controlled through 16 latched toggles mapped to
addresses <code>$C0<var>Z</var>0</code> through <code>$C0<var>Z</var>F</code>
where <code><var>Z</var></code> is the slot number + 8.

This is achieved using an index addressing mode with `SLOT16` (16 times the
slot number) in `X`: e.g. `LDA $C089,X`.

The first eight of these turn off or on different stepper phases. 

<table class="table">
  <tr><td><code>$C0<var>Z</var>0</code></td><td>Phase 0 OFF</td></tr>
  <tr><td><code>$C0<var>Z</var>1</code></td><td>Phase 0 ON</td></tr>
  <tr><td><code>$C0<var>Z</var>2</code></td><td>Phase 1 OFF</td></tr>
  <tr><td><code>$C0<var>Z</var>3</code></td><td>Phase 1 ON</td></tr>
  <tr><td><code>$C0<var>Z</var>4</code></td><td>Phase 2 OFF</td></tr>
  <tr><td><code>$C0<var>Z</var>5</code></td><td>Phase 2 ON</td></tr>
  <tr><td><code>$C0<var>Z</var>6</code></td><td>Phase 3 OFF</td></tr>
  <tr><td><code>$C0<var>Z</var>7</code></td><td>Phase 3 ON</td></tr>
</table>

To move the head inward, the phases are turned on and off in ascending order
at a particular timing. To move the head outward, the same is done in
descending order.

There are 70 positions the head can take but data written from adjacent
positions can interfere with each other and so the usable positions must be
separated. In practice, Apple DOS used the even positions (although one
copy-protection tactic was to use odd positions or some other pattern
that avoided adjacent positions).

The next eight toggles were as follows:

<table class="table">
  <tr><td><code>$C0<var>Z</var>8</code></td><td>Motor OFF</td></tr>
  <tr><td><code>$C0<var>Z</var>9</code></td><td>Motor ON</td></tr>
  <tr><td><code>$C0<var>Z</var>A</code></td><td>Select Drive 1</td></tr>
  <tr><td><code>$C0<var>Z</var>B</code></td><td>Select Drive 2</td></tr>
  <tr><td><code>$C0<var>Z</var>C</code></td><td>Strobe Data Latch</td></tr>
  <tr><td><code>$C0<var>Z</var>D</code></td><td>Load Data Latch</td></tr>
  <tr><td><code>$C0<var>Z</var>E</code></td><td>Ready Latch for Read</td></tr>
  <tr><td><code>$C0<var>Z</var>F</code></td><td>Ready Latch for Write</td></tr>
</table>

We will cover these in more detail as we encounter them.

## Seeking Track Zero

Rather than precisely move the head to track zero on boot, the disk controller
just moves the head out by 80 positions. This guarantees it is in the outermost
position regardless of its starting point. This is also what causes the
distinctive thunk-thunk-thunk sound on disk boot as the head repeatedly hits a
rubber stopper designed to prevent it moving too far.

At this point in the code, we’ve just calculated `SLOT16` and it is still in
the accumulator. We transfer it to `X`:

```
Cs2E: AA            TAX
```

We ready the latch for reading and strobe it.

```
Cs2F: BD 8E C0      LDA $C08E,X
Cs32: BD 8C C0      LDA $C08C,X
```

Then we select drive 1 and spin up the motor.
```
Cs35: BD 8A C0      LDA $C08A,X
Cs38: BD 89 C0      LDA $C089,X
```

We want to loop 80 times, so we put that in `Y`:

```
Cs3B: A0 50         LDY #80
```

We turn off the Phase 0 stepper motor. Remember that initially `X` is `SLOT16`.

```
Cs3D: BD 80 C0      LDA $C080,X
```

Note that on subsequent steps of the loop, `X` will be `SLOT16` plus 2 × PHASE.
We’re now at the part of the code that will calculate this.

We take the loop index (in `Y`) modulo 4 (to get the phase) and
double it (to get the low four bits of the address to toggle).

```
Cs40: 98            TYA
Cs41: 29 03         AND #$03
Cs43: 0A            ASL
```

When `Y` is `80`, we get `0`; when `Y` is `79`, we get `6`; when `Y` is `78`,
we get `4`; then `2`; then back to `0` and so on. In other words, 2 × PHASE.
And because `Y` is decrementing, we are cycling through the phases in descending
order which means the head will move outwards.

`SLOT16` is also in zero-page `$2B` so lets combine that with the 2 × PHASE.

```
Cs44: 05 2B         ORA $2B
Cs46: AA            TAX
```

Now `X` is `SLOT16` + 2 × PHASE, which is exactly what we need to turn on
that stepper motor phase.

```
Cs47: BD 81 C0      LDA $C081,X
```

Now the timing is important. We need to wait about 20 milliseconds. There is
a `MON_WAIT` routine in the monitor (`$FCA8`) that consumes cycles as a quadratic
function of the accumulator (the number of cycles is 2.5`A`² + 13.5`A` + 7).

We set `A` to `#$56` and call `MON_WAIT` which will consume a total of 19,664
cycles including the `JSR`.

```
Cs4A: A9 56         LDA #$56
Cs4C: 20 A8 FC      JSR MON_WAIT
```

We now decrement the index and loop.

```
Cs4F: 88            DEY
Cs50: 10 EB         BPL $Cs3D
```

Once we’ve moved the head out, we set up some more zero-page values.

Note that `A` is now `#$00` because that’s what it ends up as after a `MON_WAIT`.

```
Cs52: 85 26         STA $26
Cs54: 85 3D         STA $3D
Cs56: 85 41         STA $41
Cs58: A9 08         LDA #$08
Cs5A: 85 27         STA $27
```

So this puts `#$0800` into `$26`/`$27` (the location of the data better to load
the first sector into) and `#$00` into `$3D` (the sector to load) and `$41` (the
track to load).

## Looking for Headers

With our drive head on the outermost track, we’re now going to read bytes until
we see what’s known as the **address header**. We’ll then check we’ve got track
0 and sector 0 and, then look for the **data header** and load in the data.

Whether we’re looking for the address header or the subsequent data header is
captured in the carry flag.

Because we want to find the address header first, we clear the carry and store
the flags on the stack.

```
Cs5C: 18            CLC
Cs5D: 08            PHP
```

Next we strobe the latch until the high bit is on (which indicates data has
been read).

```
Cs5E: BD 8C C0      LDA $C08C,X
Cs61: 10 FB         BPL $Cs5E
```

Then we test whether it is `#$D5` and, if not, loop back and read again.

```
Cs63: 49 D5         EOR #$D5
Cs65: D0 F7         BNE $Cs5E
```

It is important to note that the actual bytes read off disk into the latch
are not the actual bytes we’re ultimately going to load into memory. The data
is encoded to get around certain physical limitations in the hardware. We’ll
shortly get into two types of encoding used.

Both the address header and data header start with `$D5` so that’s what we
initially look for. It is not actually possible to get a `$D5` in either of
the encodings used and so a `$D5` can only mean the start of a header.

The next byte, whether an address header or data header, is always `$AA`.

We loop until we get the high bit set on the latch.

```
Cs67: BD 8C C0      LDA $C08C,X
Cs6A: 10 FB         BPL $Cs67
```

Then we compare what we get with `#$AA`. Notice this time we use `CMP` not `EOR`.
That is because we want to keep the value in `A` (`EOR` is destructive).
If we didn’t get an `$AA` we jump back to see if we actually got another `$D5`.

```
Cs6C: C9 AA         CMP #$AA
Cs6E: D0 F3         BNE $Cs63
Cs70: EA            NOP
```

If we did get an `$AA`, we continue. It’s not clear why there is an `NOP` here.

We read the third byte

```
Cs71: BD 8C C0      LDA $C08C,X
Cs74: 10 FB         BPL $C6s71
```

and compare it to `#$96`.

```
Cs76: C9 96         CMP #$96
Cs78: F0 09         BEQ $Cs83
```

If so, we have an address header `D5 AA 96` and jump to `$Cs83` to handle it.

Note that we do this _even if we were looking for a data header_ because it
means we’ve hit a new sector and need to check if it’s the right one.

But if we got a `D5 AA` that isn’t followed by a `96`, what we do next does
depend on whether we’re looking for data and so we pull the status and if we
were actually looking for an address header (i.e. the carry flag is clear),
we'll start the whole process again.

```
Cs7A: 28            PLP
Cs7B: 90 DF         BCC $Cs5C
```

But if we are looking for data, we check if we got a `#$AD` (because a data
header starts with `D5 AA AD`). If so, we branch to `$CsA6` to handle the data.
Otherwise we go back and keep looking.

```
Cs7D: 49 AD         EOR #$AD
Cs7F: F0 25         BEQ $CsA6
Cs81: D0 D9         BNE $Cs5C
```

It is worth noting here what each of `D5`, `AA`, `96`, and `AD` look like in
binary:

<table class="table">
  <tr><td><code>D5</code></td><td><code>11010101</code></td></tr>
  <tr><td><code>AA</code></td><td><code>10101010</code></td></tr>
  <tr><td><code>96</code></td><td><code>10010110</code></td></tr>
  <tr><td><code>AD</code></td><td><code>10101101</code></td></tr>
</table>

TO BE CONTINUED
