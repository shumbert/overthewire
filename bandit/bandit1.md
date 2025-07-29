Interesting, here there is a file called `-`.

If you do `cat -` it just tries to read stdin. However if you do `cat ./-` it reads the file.
