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
rubber stopped designed to prevent it moving too far.

At this point in the code, we’ve just calculated `SLOT16` and it is still in
the accumulator. We transfer it to `X`:

```
C62E: AA            TAX
```

We ready the latch for reading and strobe it.

```
C62F: BD 8E C0      LDA $C08E,X
C632: BD 8C C0      LDA $C08C,X
```

Then we select drive 1 and spin up the motor.
```
C635: BD 8A C0      LDA $C08A,X
C638: BD 89 C0      LDA $C089,X
```

We want to loop 80 times, so we put that in `Y`:

```
C63B: A0 50         LDY #80
```

We turn off the Phase 0 stepper motor. (Remember that initially `X` is `SLOT16`.)

```
C63D: BD 80 C0      LDA $C080,X
```

We now take the loop index (in `Y`) modulo 4 (to the get the phase) and
double it (to get the low four bits of the address to toggle).

```
C640: 98            TYA
C641: 29 03         AND #$03
C643: 0A            ASL
```

When `Y` is `80`, we get `0`; when `Y` is `79`, we get `6`; when `Y` is `78`,
we get `4`; then `2`; then back to `0` and so on. In other words, 2 * PHASE.

`SLOT16` is also in zero-page `$2B` so lets combine that with the 2 * PHASE.

```
C644: 05 2B         ORA SLOT16
C646: AA            TAX
```

Now `X` is `SLOT16` + 2 * PHASE, which is exactly what we need to turn on
that stepper motor phase.

```
C647: BD 81 C0      LDA $C081,X
```

Now the timing is important. We need to wait about 20 milliseconds. There is
a `MON_WAIT` routine in the monitor (`$FCA8`) that consumes cycles as a quadratic
function of the accumulator (the number of cycles is 2.5 * A**2 + 13.5 * A +7).

We set `A` to `#$56` and call `MON_WAIT` which will consume a total of 19,664
cycles including the `JSR`.

```
C64A: A9 56         LDA #$56
C64C: 20 A8 FC      JSR MON_WAIT
```

We now decrement the index and loop.

```
C64F: 88            DEY
C650: 10 EB         BPL $C63D
```
