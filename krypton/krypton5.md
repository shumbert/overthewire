# Overview
Here the instructions says:
```
Frequency analysis can break a known key length as well.  Lets try one
last polyalphabetic cipher, but this time the key length is unknown.
```

And then it provides a number of ciphertexts encrypted with the same key.

# Breaking the code
I updated the script for the previous exercise, and added an argument for the key length. Now, if the script is run with an incorrect key length I get unexpected results: all the letters have more or less the same frequency. However, when running the script with a key length of 9 I see the usual pattern, with one letter from the ciphertext being significantly more frequent than the others (and so probably encrypting the plaintext letter `E`).

Ok, so the key length is 9. Now I just need to do frequency analysis for the various ciphertext positions. As the ciphertext to decrypt is only 6 characters long, we only need to find out the key for the first 6 positions. Anyway, eventually I find out the key starts with `keylen`.

Password for the next level is `RANDOM`.
