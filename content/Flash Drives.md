{
	"Title": "Flash Drives",
	"Abstract": "", 
	"Parents": ["Hard Drives"], 
	"Children": ["Floating-Gate Transistors","Capacitors"] ,
    "Date": "2020-08-10"
}


# Flash Drives

## The flash memory

The flash memory is a kind of memory that is faster and has a smaller form factor than magnetic drives. Its principle of operation is basically based on the DRAM (See <a href="Random Access Memories.html">Random Access Memories</a>) but with different electronic components; that allows it to be persistent (without the need of a refresh mechanism): the floating-gate (FG) transistors.

## Architecture

The flash memories combine many of these FG transistors into arrays, in a similar way as in random access memories. Different layouts exist, but the two main layouts are called *NOR Flash* and *NAND Flash*.

In a memory, such as SRAM, DRAM or flash, we usually use two electronic lines to read or write the data at a specific location. These two lines are called the *bit line* and the *word line*. When we have an array of memory cells, each column corresponds to a word line and each row of the array corresponds to a bit line. To read the content of a specific cell, we just apply or read the voltage/current between the corresponding word and bit lines.

The NOR flash design connects one end of all cells to the ground while the other end is connected to a bit line. The word line is connected on the control gates of the FG transistors. This creates an array of structures that resembles a NOR gate (for Not-OR).

The NAND flash design connects all the FG transistors in series, such that the bit line voltage will be low only if all the word lines (connected to the control gates) are high at the same time (which resembles the way NAND gates operate).

## Reading / Writing

Flash memories have a surprising property when it comes to writing data. In a flash memory, you can read the data, write a single bit from bit 1 to bit 0, but you cannot write a single bit from bit 0 to bit 1; due to the architecture that connects the flash cells together. This process is called earsing, and is only possible by doing it on an entire block of memory, usually consisting of some kilobytes to megabytes of size. 

One of their disadvantages is also wear. A single FG transistor wears out after between 10,000 and 1 million read/write operations. This problem is partially solved by using controllers that use the full available storage when writing data so that single cells do not wear out too quickly. 