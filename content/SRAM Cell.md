{
    "Title": "SRAM Cell",
    "Abstract": "",
    "Parents": ["Processor Cache Memories"],
    "Children": ["MOSFET Transistors"],
    "Date": "2021-05-08"
}

# Static Random Access Memory Cell


The SRAM is the main memory used as cache memory in processors. Its fundamental building block is composed of 6 transistors, that are connected to form 2 logic inverters (using 4 transistors) and 2 control transistors allowing to access the data for reading and writing. Below is the electrical schematic representing an SRAM cell.

<img src="images/articles/SRAM-Cell.png" class="w3-center" width="60%" />

M1, M2 and M3, M4 are the transistors that form the two inverters. M5 and M6 are the control transistors. To write a bit into the memory cell, the couple of inverters are forced into a state, either with <M1, M2> inverter output to high or low, by applying a slightly higher voltage that would normally be used for these components. Once the state has been written, it can be read by opening the transistors M5 and M6 and reading the lines BL and BL bar. 

As opposed to the DRAM memory, SRAM do not need any refresh mechanism as long as the power is maintained in the circuit. When the inverters are in a given state, it will stay as long as the power is maintained: when the output of the first inverter is high, the input of the second inverter is high, which generates a low-signal at its output. This low-signal is directed again to the input of the first inverter. 

This memory is more expansive and faster, so it is usually not used as the main memory of computers but rather as the processor cache memory. 