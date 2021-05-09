{
    "Title": "DRAM Cell",
    "Abstract": "",
    "Parents": ["Random Access Memories"],
    "Children": ["MOSFET Transistors", "Capacitors"],
    "Date": "2020-08-24"
}

# Dynamic Random Access Memories

The DRAM is the main memory used as a working memory in computers. The fundamental building block of a DRAM is composed of a transistor -- that allows addressing the bit for reading / writting -- and a capacitor -- that stores the information. Its electrical schematic is shown below.

<table class="w3-center" width="100%">
	<tr><th>
		<img src="images/articles/DRAM.svg" class="w3-center" width="60%" />
	</th></tr>
</table>

This consists of what is called a memory cell. Storing a bit -- 1 or 0 -- means charging or discharging the capacitor in this memory cell. To read the content of a cell, the transistor is opened and the capacitor current charge is read. These memory cells are usually arranged in a rectangle that can go to thousands of cells in width and height.

Due to inherant characteristics of capacitors, these devices are prone to electrical leakage and easily discharge over time. This has to be compensated by constantly re-writing the data stored in a DRAM. This is usually done every tenth of miliseconds (see the <a href="https://www.jedec.org">JEDEC standard</a>). 

When starting a program on a computer, the operating system loads the entier program instructions from the hard drive into the DRAM memory. It is then executed from this memory and into the processor, transiting by the processor's cache memory. 