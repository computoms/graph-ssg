{
    "Title": "Why Twos Complement",
    "Abstract": "Why Two's Complement Representation?",
    "Parents": ["Negative Numbers"],
    "Children": [""],
    "Date": "2020-11-22"
}

# The Reason behind Two's Complement Representation

Why are we using such a complicated formula? Because the goal of computers is to compute (perform operations on numbers) and this representation helps our electronic components handle the data. For example, using the two's complement reprsentation it is straightforward to add two numbers. The addition rule is the same as with positive numbers (adding bits one by one with the carry):

<table class="w3-table-all w3-hoverable">
	<tr class="w3-green">
		<td>Decimal addition</td>
		<td>Binary addition</td>
		<td>Binary result</td>
		<td>Decimal result</td>
	</tr>
	<tr class="w3-hover-green">
		<td>6 + (-4)</td>
		<td>0110 + 1100</td>
		<td>(1)0010</td>
		<td>2</td>
	</tr>
</table>

The second advantage of this representation is we can easily implement subtraction: to perform a - b, we only need to transform b into its two's complement representation and then add the two numbers a + (-b).
