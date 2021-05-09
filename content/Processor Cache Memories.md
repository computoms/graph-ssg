{
    "Title": "Processor Cache Memories",
    "Abstract": "",
    "Parents": ["Computer Memories"],
    "Children": ["SRAM Cell"],
    "Date": "2020-09-14"
}

# Processor Cache Memories

In order to have an even faster memory, processors implement a part of memory directly onto their chips, called the cache memory. Its hardware implementation and location (closer to logic area of the processor) makes it the fastest storage accessible from the processor. This memory is also a type of random access memory, and shares its drawbacks (loss of data when power turns off).

Before data is loaded into processor registers from the RAM memory, it is actually transferred from RAM to cache memory. Knowing this is important to understand the performance of data structures and of some algorithms.
