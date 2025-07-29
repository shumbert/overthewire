# Overview
The instructions mention the cipher used is the [Vigenere cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher), and that the key is 6 characters long.

Essentially, with the Vigenere cipher each letter of the plaintext is encoded with a different Caesar cipher, whose increment is determined by the corresponding letter of the key.

In addition to instructions, we have multiple ciphertexts encrypted with the same key as the text to decrypt.

# Breaking the code
So the idea is to do frequency analysis for each position of the key. Each time, we only need to isolate the letter with the highest frequency. As `E` is the letter with the highest frequency in English (by a significant margin), it should give us the increment. Check out the krypton4.py script for further details. Eventually I found out that the key is `frekey`.

Password for the next level is `CLEARTEXT`.
