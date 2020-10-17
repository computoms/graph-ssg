{
    "Title": "UTF-8",
    "Abstract": "",
    "Parents": ["UTF"],
    "Children": [""]
}

# UTF-8

To overcome the problems of memory space explained in UTF-32, the UTF-8 encoding has been invented.

The UTF-8 is a variable bit-length format that takes at minimum 1 byte of memory for each character, but can go up to 4 bytes of memory for a single character (see Storing Numbers).

The principle behind the encoding uses the fact that ASCII only uses 7 bits to store its characters (up to number 127), so we can use the remaining bit to say if we are storing ASCII (last bit is 0) or if we are using more bytes to store an extra character (last bit is 1). In the latter case, we'll set each following bits to 1 to indicate the length of our character in bytes and the next bit will be set to 0 as a separator. For example, if we see the first byte of UTF-8 encoded string that is 110x xxxx it means that it is a character that is encoded in two bytes. Here is a table that summarizes the possible scenarios for UTF-8 encoded characters:

Number of bytes	Byte 1	Byte 2	Byte 3	Byte 4
1	0xxxxxxx			
2	110xxxxx	10xxxxxx		
3	1110xxxx	10xxxxxx	10xxxxxx	
4	11110xxx	10xxxxxx	10xxxxxx	10xxxxxx

By using a variable length enconding like this one, we are saving space on the memory. This encoding is one of the most used encoding for storing strings of characters in programs and websites.