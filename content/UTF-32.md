{
    "Title": "UTF-32",
    "Abstract": "",
    "Parents": ["UTF"],
    "Children": [""],
    "Date": "2020-12-21"
}

# UTF-32

The ASCII encoding is using numbers from 0 to 127 to store the English alphabet and letters. As explained in Storing Numbers, these numbers are stored using a fixed amount of memory, that is called a byte (taking 8-bits of memory space); and is limited to numbers below 256.

In order to extend the alphabet to other symbols, we need to convert these symbols to numbers that are higher than 256. The UTF-32 encoding uses numbers up to 4294967296 (that is a lot!) in a number format that takes 32-bits of memory space.

## Advantages

The advantages of this encoding is that it is retro-compatible with ASCII: the first 127 characters are equivalent in both encodings.

## Drawbacks

The drawbacks is that if you store mostly English alphabet's characters, you are loosing memory space because each number will take the same amount of space in this encoding, whatever its value (which will be 32 bits of memory space for each character, as compared to just 8-bits for ASCII encoding characters).