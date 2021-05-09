{
    "Title": "AND Gate",
    "Abstract": "",
    "Parents": ["Logic Circuits"],
    "Children": [""],
    "Date": "2020-06-22"
}

# AND Gate

The AND Gate is a logic gate, an electronic component that can perform logic operations on the voltage it is applied on its input pins. It allows to apply the AND logic operation on its two input pins.

Here is the electronic schematics of the AND gate:

<table class="w3-center" width="100%">
	<tr><th>
		<img src="images/articles/Gate-AND.svg" class="w3-center" width="60%" />
	</th></tr>
</table>

We can see that pretty simply, the only possibility to have a high voltage at the output (Out) is to have both A and B signals high. If one of them is low, the Vdd signal will not be able to come to the Out, but one of the Vss will pass through the PMOS transistors of the bottom. This represents the AND logic.
