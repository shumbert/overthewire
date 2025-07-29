Page has a link to its source code including the following PHP code:
```
<?

$encodedSecret = "3d3d516343746d4d6d6c315669563362";

function encodeSecret($secret) {
    return bin2hex(strrev(base64_encode($secret)));
}

if(array_key_exists("submit", $_POST)) {
    if(encodeSecret($_POST['secret']) == $encodedSecret) {
    print "Access granted. The password for natas9 is <censored>";
    } else {
    print "Wrong secret";
    }
}
?>
```

So we need to reverse the operations above:
- start at $encodedSecret
- convert the hexadecimal bytes to an ASCII string
- reverse the string
- Base64 decode it

You can do all the operations above with Cyberchef.

Password for the next level is `ZE1ck82lmdGIoErlhQgWND6j2Wzz6b6t`.
