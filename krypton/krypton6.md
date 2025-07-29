# Overview
Instructions here are lengthy and confusing, even misleading. It covers stuff on block ciphers, then switches to stream ciphers and one-time pads. It also says that we are now working with bytes, not ASCII text, so a hex editor is required. It also says that the use of cryptools is recommended.

We have the following files:
- krypton7: the ciphertext to decrypt
- encrypt6: encryption binary
- keyfile.dat: the encryption key

encrypt6 uses the encryption key and a (weak) random number to generate a keystream that is used to encrypt the plaintext.

There is a file HINT1 which says:
```
The 'random' generator has a limited number of bits, and is periodic.
Entropy analysis and a good look at the bytes in a hex editor will help.

There is a pattern!
```

And a file HINT2 which says:
```
8 bit LFSR
```

# Playing with encrypt6
I played a bit with encrypt6, encrypting the plaintext `aaaaaaaaaaaaaaa` yields:
```
EICTDGYIYZKTHNS
```

Running it multiple times yields the same result. Also something important, encrypting the plaintext `AAAAAAAAAAAAAAA` also yields `EICTDGYIYZKTHNS`. I thought initially that encrypt6 would generate a keystream made of bits and then XOR it with the plaintext, but it actually generate a stream of letter shifts. So much for working with bytes...

# Cracking the code
I don't understand that stuff about entropy analysis and weak random generator, we just need to reverse the letter shifts.

Password for the next level is `LFSRISNOTRANDOM`.
