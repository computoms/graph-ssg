{
    "Title": "Fractional Numbers",
    "Abstract": "",
    "Parents": ["Number Encodings"],
    "Children": ["Single Precision Numbers", "Double Precision Numbers"],
    "Date": "2020-10-26"
}

# Fractional Numbers

Until now, we saw how to store integer numbers. But how to store fractional numbers, such as 2.34? We need a different encoding for these numbers: the floating-point format. We are usually representing fractional numbers in two sizes: 32 bits (`float` type in C) and 64 bits (`double` type in C).

Recall how to construct a decimal number using powers of tens. For fractional numbers, it is the same, but with negative powers of tens after the comma: the number 12.345 can be written:

12.345 = 1 * 10^1 + 2 * 10^0 + 3 * 10^(-1) + 4 * 10^(-2) + 5 * 10^(-3)

We can use the same approach to represent a binary number:

1100.101_2 = 1 * 2^3 + 1 * 2^2 + 0 * 2^1 + 0 * 2^0 + 1 * 2^(-1) + 0 * 2^(-2) + 1 * 2^(-3)

The idea behind encoding floating point numbers is like representing the numbers in scientific notation. Scientific notation, in decimal, is the representation of any number in the form

number = y.xxx * 10^e

for example: 1 345 673.12 = 1.34567312 * 10^6

Thus the binary number scientific notation would be:

number_2 = 1.xxx * 2^e

for example: 1100.101_2 = 1.100101_2 * 2^(11_2)

This is what is used to encode fractional binary numbers: \pm 1.[fraction] * 2^([exponent]).