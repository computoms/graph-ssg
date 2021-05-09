{
    "Title": "Negative Numbers",
    "Abstract": "",
    "Parents": ["Number Encodings"],
    "Children": ["Why Twos Complement"],
    "Date": "2020-11-02"
}

# Negative Numbers

In mathematics, we are representing the negative numbers using the minus sign `-`. In computer hardware, there's no such thing. Only 0 and 1, so we needed to find a way to encode our negative numbers in binary form without using an extra symbol.

## The Two's Complement Encoding

There are several ways to encode a negative number into binary, but the main technique that is used nowadays by processors is called two's complement.

Let's take a 4-bits chuck of memory as an example. In regular encoding, as seen above, this chunk can store numbers from 0 (0000 in binary) to 15 (1111 in binary). With 4 bits, we can only store 16 different values, so the idea with the two's complement method is to shift the values in order to represent numbers from -8 to 7 instead - so that we can represent negative numbers.

The two's complement method goes like this: for each strictly positive number, you can find it's negative counter-part by inverting all its bits and adding one. For example:

<table class="w3-table-all w3-hoverable">
	<tr class="w3-green">
		<td>Number (base 10)</td>
		<td>4-bits binary</td>
		<td>Negative (base 10)</td>
		<td>Two's complement</td>
	</tr>
	<tr class="w3-hover-green">
		<td>1</td>
		<td>0001</td>
		<td>-1</td>
		<td>1110 + 0001 = 1111</td>
	</tr>
	<tr class="w3-hover-green">
		<td>2</td>
		<td>0010</td>
		<td>-2</td>
		<td>1101 + 0001 = 1110</td>
	</tr>
	<tr class="w3-hover-green">
		<td>3</td>
		<td>0011</td>
		<td>-3</td>
		<td>1100 + 0001 = 1101</td>
	</tr>
	<tr class="w3-hover-green">
		<td>7</td>
		<td>0111</td>
		<td>-7</td>
		<td>0110 + 0001 = 0111</td>
	</tr>
</table>


This also works the other way around:

<table class="w3-table-all w3-hoverable">
	<tr class="w3-green">
		<td>Number (base 10)</td>
		<td>4-bits binary</td>
		<td>Negative (base 10)</td>
		<td>Two's complement</td>
	</tr>
	<tr class="w3-hover-green">
		<td>-1</td>
		<td>1111</td>
		<td>1</td>
		<td>0000 + 0001 = 0001</td>
	</tr>
	<tr class="w3-hover-green">
		<td>-2</td>
		<td>1110</td>
		<td>2</td>
		<td>0001 + 0001 = 0010</td>
	</tr>
	<tr class="w3-hover-green">
		<td>-3</td>
		<td>1101</td>
		<td>3</td>
		<td>0010 + 0001 = 0011</td>
	</tr>
	<tr class="w3-hover-green">
		<td>-7</td>
		<td>1001</td>
		<td>7</td>
		<td>0110 + 0001 = 0111</td>
	</tr>
</table>

There are two special cases, though: 0 and -8:

<table class="w3-table-all w3-hoverable">
	<tr class="w3-green">
		<td>Number (base 10)</td>
		<td>4-bits binary</td>
		<td>Two's complement</td>
	</tr>
	<tr class="w3-hover-green">
		<td>0</td>
		<td>0000</td>
		<td>0000</td>
	</tr>
	<tr class="w3-hover-green">
		<td>-8</td>
		<td>1000</td>
		<td>1000</td>
	</tr>
</table>

More formally, the two's complement b of a binary number a encoded using n bits is the binary number such that a + b = 2^n with n the number of bits that encodes a and b. Thus, b = 2^n - a, and we can find our two special cases:

<table class="w3-table-all w3-hoverable">
	<tr class="w3-green">
		<td>4-bit number a</td>
		<td>Two's complement (base 10)</td>
		<td>Two's complement on 5-bits</td>
		<td>4-bit Two's complement</td>
	</tr>
	<tr class="w3-hover-green">
		<td>0000</td>
		<td>16 - 0 = 16</td>
		<td>10000 - 00000 = 10000</td>
		<td>0000</td>
	</tr>
	<tr class="w3-hover-green">
		<td>1000</td>
		<td>16 - 8 = 8</td>
		<td>10000 - 01000 = 01000</td>
		<td>1000</td>
	</tr>
</table>

As you can see, overflowing bits are thrown away (the fifth bit cannot be stored as we are using 4 bits to stored our numbers).


















