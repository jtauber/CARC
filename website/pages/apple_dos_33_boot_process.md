---
title: Apple DOS 3.3 Boot Process
---
I’m going to sketch out the Apple DOS 3.3 boot process here.
These are work-in-progress notes.

`BOOT0` the code on the ROM chip on the disk drive controller card.  
`BOOT1` the code on the boot sector of the floppy.


## Calculating `SLOT16`

`BOOT1` assumes that zero-page `$2B` (which we’ll call `SLOT16`) contains the
slot number of the disk drive controller card times 16. How does that get there?
Well, there’s some interesting code in `BOOT0` that sets it.

The way I/O is mapped on the Apple II, the 256-byte ROM on a card in slot `s` is
addressable as `$Cs00`. So a disk drive controller in slot 6 (the default) has its
ROM mapped to `$C600`-`$C6FF`.

That means that if code on that ROM knew its own address, it could work out what
slot the card is in. How does code work out its own address? Well, it can can rely
on the fact that if you jump to a subroutine, the address to return to
(technically one byte before) is put on the stack. 

So what `BOOT0` does is a `JSR` to a location in the Monitor ROM that just
contains an `RTS`.

```
Cs21: 20 58 FF      JSR MON_RTS
```

This puts (one less than) the return address (i.e. `$Cs23`) on the stack and
does the jump. At this point the stack will look like:

```
0100                    STACK
...
01FD               <--- STACK + S
01FE            23
01FF            Cs
```

where `STACK` is the start of the stack and `S` is the stack register that
points to the next spot to push something to.

After the jump, we immediately return (pulling one less than the return address
off the stack) and the stack memory looks like:

```
0100                    STACK
...
01FE            23
01FF            Cs <--- STACK + S
```

Note that `$Cs23` is still in stack memory
(although it will be overwritten the next time something is pushed onto the stack).

We want the value at `STACK + S` so we transfer the `S` register to the `X` register:

```
Cs24: BA            TSX
```

We then load into `A` the value the stack pointer is pointing at:

```
Cs25: BD 00 01      LDA STACK,X
```

Now `A` contains `Cs`.

We just need to shift that left four times with `ASL` and that gives us `s * 16`.

```
Cs28: 0A            ASL
Cs29: 0A            ASL
Cs2A: 0A            ASL
Cs2B: 0A            ASL
```

We then store that in zero-page address `$2B` (`SLOT16`).

```
Cs2C: 85 2B         STA SLOT16
```

## Setting up the Sector Read Call

Back over in `BOOT1` we want to establish the address of the routine to read a sector.
We’re ultimately going to put it in `$3E/$3F`.

This routine lives at `$Cs5C` but we need to know `s` (the slot) to calculate that address.

So we load `SLOT16` from the zero-page address it has been put in:

```
0807: A5 2B         LDA SLOT16
```

Then we shift right four times to _divide_ by 16:

```
0809: 4A            LSR
080A: 4A            LSR
080B: 4A            LSR
080C: 4A            LSR
```

Now `A` contains the slot number `s` of the disk driver controller.

We logically OR this with `#$C0` to get `#$Cs`:

```
080D: 09 C0         ORA #$C0
```

and store it in `$3F`.

```
080F: 85 3F         STA $3F
```

We then load `A` with `#$5C`

```
0811: A9 5C         LDA #$5C
```

and store it in `$3E`

```
0813: 85 3E         STA $3E
```

Now `$3E/$3F` contains `$Cs5C` (e.g. `$C65C` if the card is in slot 6).

## Setting up the Read Buffer Address and Number of Sectors to Read

The very end of the `BOOT1` boot sector contains three bytes of data:

```
08FD: 00
08FE: B6
08FF: 09
```

`$08FD/$08FE` contains the start address that the sectors are be loaded into (i.e. `$B600`).

`$08FF` contains highest sector number to read. As we start on sector 0, the highest number being 9 means 10 sectors in total.

The first sector (sector 0, the one we’re already on) will be loaded into `$B600`-`$B6FF`, the second into `$B700`-`$B7FF`, and so on up to `$BF00`-`$BFFF`.

The code that prepares for that read using this data is as follows.

Firstly, because we’re going to add-with-carry (`ADC`) we want to make sure the carry flag `C` is cleared:

```
0815: 18            CLC
```

Then we load the high byte of the read buffer address.

```
0816: AD FE 08      LDA $08FE
```

and add the number of sectors to read (`#$09`).

```
0819: 6D FF 08      ADC $08FF
```

We then put the calculated value (now `#$BF`) back into `$08FE`.

```
081C: 8D FE 08      STA $08FE
```

So now `$08FD`/`$08FE` contains `$BF00`. This is because we’re going to read the sectors last first. We’ll load sector 9 into `$BF00`-`$BFFF` first, then sector 8 into `$BE00`-`$BEFF`, and so on down to loading sector 0 into `$B600`-`$B6FF`.

Why do we bother loading sector 0 at `$B600` if we’ve already loaded it at `$0800` and are executing it now? We won’t
need to run the code again, but having it at `$B600` means it’s available later use in the initialization of new bootable disks.

## Reading in Each Sector with `BOOT1`

Now let’s look at the loop that loads the sectors.

`$08FF` contains the sector to read so we firstly load that into register `X`.

```
081F: AE FF 08      LDX $08FF
```

Then we check if we’ve gone below zero and, if so, branch out of the loop.

```
0822: 30 15         BMI $0839
```

Now the logical sector is not actually the raw sector number used on disk because of the interleaving that is done.
We need to map the logical sector number to the raw sector to actually pass to the Sector Read Routine.

This mapping is done at `$084D`:

```
084D: 00 0D 0B 09 07 05 03 01 0E 0C 0A 08 06 04 02 0F
```

In other words, the raw sector number for logical sector `#$09` is `#$0C` which is found at `$084D` + `$09`.

And so we use this table to load the raw sector number into `A`:

```
0824: BD 4D 08      LDA $084D,X
```

and store it in `$3D`, the zero-page address used by the routine in `BOOT0`.

```
0827: 85 3D         STA $3D
```

We then decrement `$08FF` (the next sector to read):

```
0829: CE FF 08      DEC $08FF
```

Next up is to set the zero-page address for where the routine is to load the sector into. This is `$26`/`$27`.
The low-byte is always `#$00` so doesn’t need to be set but the high-byte should be whatever is in `$08FE` and so we
load `$08FE` into `A:

```
082C: AD FE 08      LDA $08FE
```

and store it in `$27`:

```
082F: 85 27         STA $27
```

Then we can decrement the high-byte of that address for the next iteration:

```
0831: CE FE 08      DEC $08FE
```

Finally we load `X` with `SLOT16` (`$2B`):

```
0834: A6 2B         LDX $2B
```

and indirectly call the sector read routine whose address we have stored in `$3E`/`$3F`:

```
0836: 6C 3E         JMP ($3E)
```

Notice this is a `JMP` not `JSR`. How does the code return? Well, we’ll see in more detail when we dive into that
part of the `BOOT0` code but basically when the sector is loaded, that routine jumps to `$0801` which is the start
of the `BOOT1` code and we’ll cover that in a moment, once we’ve looked at what happens at the end of the `BOOT1` process.

## Finishing Up `BOOT1`

Once the sector number has been decremented below zero, we branch out of the loop.
At this point the high-byte of our read buffer address has been decremented below the start value (`$B6` normally) too.
We first of all increment this to bring it back.

```
0839: EE FE 08      INC $08FE
```

We then increment it again because we actually want to execute the _next_ part of the code:

```
083C: EE FE 08      INC $08FE
```

Now `$08FD`/`$08FE` should contain the address where sector 1 (the continuation of the boot process) lives.

We make a series of calls to the Monitor ROM to make sure things are initialized there:

```
083F: 20 89 FE      JSR MON_SETKBD
0842: 20 93 FE      JSR MON_SETVID
0845: 20 2F FB      JSR MON_INIT
```

We put `SLOT16` into the `X` register.

```
0848: A6 2B         LDX $2B
```

And finally jump to the address in `$08FD` (which will be `$B700` normally):

```
084A: 6C FD 08      JMP ($08FD)
```

## The Start of `BOOT1`

The only part we haven’t covered is the initial code at `$0801` that is both run initially and after each sector read.

If it’s our first time, we need to set up the sector read call, the read buffer address, and the number of sectors to read.
Otherwise we just proceed to read the next sector. How can we tell?

We rely on the fact that, immediately after `BOOT0` has loaded the boot sector into `$0800`, `$26`/`$27` will contain the next page: `#$0900`. In other words, `$27` will contain `#$09`. But once we’ve loading DOS into `$B600`-`$BFFF`, `$27` will no longer contain `#$09`.

So we firstly load `$27` into `A:

```
0801: A5 27         LDA $27
```

and then compare it to `#$09`.

```
0803: C9 09         CMP #$09
```

If it’s not equal, we’ve already loaded stuff before and can jump right to reading the next sector (otherwise we continue on to the setup).

```
0805: D0 18         BNE $081F
```
