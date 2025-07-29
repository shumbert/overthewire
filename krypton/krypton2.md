# Overview
There are two files in addition to the ciphertext and the instructions:
- encrypt
- keyfile.dat

The instructions make it look complicated, you can run `encrypt` to encrypt various cleartexts and try to figure things out.

# Pwn
But the password is just encrypted with the Caesar cipher, using a right-shift of 14.

Password for the next level is `CAESARISEASY`.
