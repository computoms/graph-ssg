{
    "Title": "Single Precision Numbers",
    "Abstract": "",
    "Parents": ["Fractional Numbers"],
    "Children": [""],
    "Date": "2020-11-15"
}

# Single Precision Numbers

On 32 bits, we divid the bits with 1 sign bit s, 8 exponent bits e and the remaining 23 bits for the fractional part:

The formula for decoding a 32-bit floating point number is as follows:

$$n_(10) = (-1)^s * 2^e * ( 1 + \sum_i b_(23-i) * 2^(-i))$$

where n_(10) is the resulting decimal number, s is the sign bit (most significant bit), e is the decimal value corresponding to the 8 exponent bits and b_i are the bits number i.

## Sign bit

The most significant bit (bit 31) is the sign bit. `0` means we encoded a positive number, and `1` is negative.

## Exponent encoding

The exponent e is not encoded using the two's complement representation, but with a different one: the offset-binary representation with the zero offset being 127. This means that 0000 \, 0000_2 represents -126, 1000 \, 0000_2 represents 0 and 1111 \, 1111_2 represents 127.

## Fraction encoding

The fractional part of the number is encoded with standard binary encoding. There is a simple method to convert a decimal fractional part into binary:

* multiply by two * take the integer part (either 0 or 1) which will be the binary bit number -1 (bit number 22 in our 32-bit floating-point encoding) * multiply the fractional part of the number obtained by 2 * repeat for bit number -2 ... -22 (bits 21 to 0 in 32-bit floating-point encoding)

For example, for 0.345:

<table class="w3-table-all w3-hoverable">
	<thead>
		<tr class="w3-green">
			<th>Multiply by 2</th>
			<th>Integer part</th>
			<th>Fraction part</th>
			<th>Bit number in 32-bit representation</th>
		</tr>
	</thead>
	<tr class="w3-hover-green"><td>0.345 * 2 = 0.690</td>	<td>0</td>	<td>0.690</td>	<td>22</td></tr>
	<tr class="w3-hover-green"><td>0.690 * 2 = 1.380</td>	<td>1</td>	<td>0.380</td>	<td>21</td></tr>
	<tr class="w3-hover-green"><td>0.380 * 2 = 0.760</td>	<td>0</td>	<td>0.760</td>	<td>20</td></tr>
	<tr class="w3-hover-green"><td>0.760 * 2 = 1.520</td>	<td>1</td>	<td>0.520</td>	<td>19</td></tr>
	<tr class="w3-hover-green"><td>0.520 * 2 = 1.040</td>	<td>1</td>	<td>0.040</td>	<td>18</td></tr>
	<tr class="w3-hover-green"><td>0.040 * 2 = 0.080</td>	<td>0</td>	<td>0.080</td>	<td>17</td></tr>
	<tr class="w3-hover-green"><td>..</td>	<td>..</td>	<td>..</td>	<td>..</td></tr>
	<tr class="w3-hover-green"><td>0.880 * 2 = 1.760</td>	<td>1</td>	<td>0.760</td>	<td>0</td></tr>
</table>

## Range and Precision

The fractional part is stored with 23 bits. This allows a precision of between 7 and 9 significant digits (2^(23) = 8 \, 388 \, 608). The exponent is stored on 8 bits, which allows numbers from 2^(-126) \approx 1.175 * 10^(-38) to 2^(127) \approx 1.701 * 10^(38).

