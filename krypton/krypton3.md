# Overview
The instructions here are a bit cryptic, however they mention the following:
- in addition to the ciphertext to decrypt, there are 3 other ciphertexts
- all plaintexts are in english, and all ciphertexts were produced from the same key

It becomes quickly apparent that the cipher is monoalphabetic substitution cipher (i.e. using a fixed key, and giving a one to one mapping of plaintext to ciphertext), and that you must frequency analysis to break the code. After a quick google search I found the following links:
- https://en.wikipedia.org/wiki/Frequency_analysis
- https://www.boxentriq.com/code-breaking/frequency-analysis: provides statistics on the ciphertext, and comparisons with plaintext english

# Breaking the code
Not exactly sure what the method is supposed to be, but I used the following approach:
- using the frequency analysis tool above, I checked the most common letters, digrams, and trigrams in the ciphertext
- `JDS` is the most common trigram by far, so I assumed it must match `the` in the ciphertext
- other letters/digrams/trigrams are not so clear but you can advance by trial and errors
- also you may see some patterns emerge and make more assumptions
- little you find out all the translations

The translations are:
```
A ~ b
B ~ o
C ~ i
D ~ h
E ~ g
F ~ k
G ~ n
H ~ q
I ~ v
J ~ t
K ~ w
L ~ y
M ~ u
N ~ r
O ~ x
Q ~ a
R ~ j
S ~ e
T ~ m
U ~ s
V ~ l
W ~ d
X ~ f
Y ~ p
Z ~ c
```

**Note:** for practical reasons, I put the translations above from uppercase to lowercase (makes it easy to distinguish already translated letters from those not yet translated)

And the decrypted plaintext is `WELL DONE THE LEVEL FOUR PASSWORD IS BRUTE`.
