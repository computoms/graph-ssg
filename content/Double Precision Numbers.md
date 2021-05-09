{
    "Title": "Double Precision Numbers",
    "Abstract": "",
    "Parents": ["Fractional Numbers"],
    "Children": [""],
    "Date": "2020-11-09"
}

# Double Precision Numbers

The `double` data type, as for double precision floating-point, is a data type encoded on 64 bits: 1 sign bit, 11 exponent bits and 52 fractional bits.

## Range and Precision

The 52 bits of the fractional part allows between 14 and 16 significant digits (2^(52) \approx 4.5 * 10^(15)). The exponent is stored on 11 bits, which allows numbers from 2^(-1023) \approx 1.11 * 10^(308) to 2^(1024) \approx 1.8 * 10^(308) although sometimes these two bounds are reserved for special purposes.