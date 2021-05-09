{
    "Title": "UTF-8",
    "Abstract": "",
    "Parents": ["UTF"],
    "Children": [""],
    "Date": "2021-01-04"
}

# UTF-8

To overcome the problems of memory space explained in UTF-32, the UTF-8 encoding has been invented.

The UTF-8 is a variable bit-length format that takes at minimum 1 byte of memory for each character, but can go up to 4 bytes of memory for a single character (see Storing Numbers).

The principle behind the encoding uses the fact that ASCII only uses 7 bits to store its characters (up to number 127), so we can use the remaining bit to say if we are storing ASCII (last bit is 0) or if we are using more bytes to store an extra character (last bit is 1). In the latter case, we'll set each following bits to 1 to indicate the length of our character in bytes and the next bit will be set to 0 as a separator. For example, if we see the first byte of UTF-8 encoded string that is 110x xxxx it means that it is a character that is encoded in two bytes. Here is a table that summarizes the possible scenarios for UTF-8 encoded characters:

<table class="w3-table-all w3-hoverable">
	<tr class="w3-green">
		<td>Number of bytes</td>
		<td>Byte 1</td>
		<td>Byte 2</td>
		<td>Byte 3</td>
		<td>Byte 4</td>
	</tr>
	<tr class="w3-hover-green">
		<td>1</td>
		<td>0xxxxxxx</td>
		<td></td>
		<td></td>
		<td></td>
	</tr>
	<tr class="w3-hover-green">
		<td>2</td>
		<td>110xxxxx</td>
		<td>10xxxxxx</td>
		<td></td>
		<td></td>
	</tr>
	<tr class="w3-hover-green">
		<td>3</td>
		<td>1110xxxx</td>
		<td>10xxxxxx</td>
		<td>10xxxxxx</td>
		<td></td>
	</tr>
	<tr class="w3-hover-green">
		<td>4</td>
		<td>11110xxx</td>
		<td>10xxxxxx</td>
		<td>10xxxxxx</td>
		<td>10xxxxxx</td>
	</tr>
</table>

By using a variable length enconding like this one, we are saving space on the memory. This encoding is one of the most used encoding for storing strings of characters in programs and websites.