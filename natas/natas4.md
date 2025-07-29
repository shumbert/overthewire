We see the following message on the page:
```
Access disallowed. You are visiting from "" while authorized users should come only from "http://natas5.natas.labs.overthewire.org/"
```

We just need to set the Referer header:
```
http -a natas4:tKOcJIbzM4lTs8hbCmzn5Zr4434fGZQm http://natas4.natas.labs.overthewire.org/ Referer:http://natas5.natas.labs.overthewire.org/
```

Password for the next level is `0n35PkggAPm2zbEpOU802c0x0Msn1ToK`.
