{
    "Title": "Data Types",
    "Abstract": "",
    "Parents": ["Storing Numbers"],
    "Children": [""],
    "Date": "2020-10-19"
}

# Data Types

A data type is a convention by which we store numbers of a fixed range (for example 0-255) with a fixed amount of memory.

For example, if we take a sheet of paper with a row of squares as our memory, we can say that we'll only store numbers up to 99. This way, each number that we want to store can take 2 squares. Storing 17 and then 5 will look like:

1    7    0    5

In computer memories, only 0s and 1s can be stored. It was decided to group these binary digits into groups of 8; and different data types were invented:

- The byte data type is stored on 8-bits and can store an integral number from 0 to 255

- The unsigned short data type is stored on 16-bits and can store an integral number from 0 to 65535

- The unsigned int data type is stored on 32-bits and can store an integral number from 0 to 4 294 967 295

- The unsigned long long data type is stored on 64-bits and can store an integral number from 0 to 18 446 744 073 709 551 615

Remark: these data type names are depending on the compiler and language used. Different names exist, but the memory length of 8, 16, 32 and 64 bits are standard.