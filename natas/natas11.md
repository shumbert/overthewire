The page has a link to its redacted source code. There is some logic to read the data cookie and apply the following operations:
- base64 decode
- xor encrypt (with an unknown key)
- json decode

Then if the decoded array has a `showpassword` key set to `yes` it outputs the next level password.

We don't know the key, however we know the cookie default value:
```
{"showpassword":"no","bgcolor":"#ffffff"}
```

And we see the cookie returned by the server:
```
HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg=
```

So we have both plaintext and ciphertext, we can xor the two together and get the key:
```
ciphertext = base64.b64decode('HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg=')
plaintext = b'{"showpassword":"no","bgcolor":"#ffffff"}'
key = bytes(a ^ b for a, b in zip(plaintext, ciphertext))[:4]
```

Here the key is `eDWo`. We can then encrypt a cookie for plaintext `{"showpassword":"yes","bgcolor":"#ffffff"}`:
```
base64.b64encode(bytes(a ^ b for a, b in zip(b'{"showpassword":"yes","bgcolor":"#ffffff"}', b'eDWoeDWoeDWoeDWoeDWoeDWoeDWoeDWoeDWoeDWoeD')))
```

And finally send it to the server:
```
http -a natas11:UJdqkK1pTu6VLt9UHWAgRZz6sVUZ3lEk http://natas11.natas.labs.overthewire.org/ 'Cookie:data=HmYkBwozJw4WNyAAFyB1VUc9MhxHaHUNAic4Awo2dVVHZzEJAyIxCUc5'
```

Password for the next level is `yZdkjAYZRd3R7tq7T5kXMjMJlOIkzDeB`.
