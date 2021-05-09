{
    "Title": "UTF",
    "Abstract": "",
    "Parents": ["Storing Characters"],
    "Children": ["UTF-32", "UTF-8", "UTF-16"],
    "Date": "2020-12-07"
}

# UTF

_Unicode Transformation Format_

The ASCII encoding is great for the English language, but what about other languages with different symbols and alphabets, such as French, Spanish or any other language with special characters such as accents and other symbols? We need another convention that can also store these different characters.

The first way to solve this problem is to extend the transformation table to these other characters: the Extended ASCII.

The Unicode encoding is a bit more than a conversion between characters and numbers: it defines the conversion between characters and code points, that are then translated into storable numbers using different techniques, called UTF-8, UTF-16 and UTF-32 (amongst others). It defines 1112064 code points corresponding to the different characters existing in the different languages on this planet.

## UTF-32

Storing characters with large numbers.

## UTF-8

How to reduce the memory footprint for texts with mostly simple characters?

## UTF-16

A trade-off between the two previous ones.