{
    "Title": "NOT Gate",
    "Abstract": "",
    "Parents": ["Logic Circuits"],
    "Children": [""],
    "Date": "2020-06-29"
}

# NOT / Inverter Gate

An inverter is a simple electronic component, part of the _logic gate_ family of components, that inverts a signal. If we have a high-signal on one side of this component (bit 1, or 5V) we'll have a low-signal on the output (bit 0, 0V). 

Connecting two MOSFET transistors of the different types in a row between Vdd and Vss (as shown below), and connecting the two gates of the transistors together as the input of the component, we'll have the output that inverts the signal. Inputting a positive voltage (Vdd), the pMOS transistor will be blocking, preventing current to flow from the upper Vdd to the output, but the nMOS transistor will be passing, making the output signal at the level of Vss. Conversely, inputting a 0 voltage (Vss), the pMOS will be passing (because the voltage on the gate will be negative with respect to the source, which is at Vdd) making the output signal to Vdd and the nMOS will be blocking. 

<table class="w3-center" width="100%">
	<tr><th>
		<img src="images/articles/Gate-NOT.svg" class="w3-center" width="60%" />
	</th></tr>
</table>