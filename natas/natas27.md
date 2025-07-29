That challenge presents the user with username and password fields, when input is submitted:
- if username is not present in the database, it is added
- if username is present and password is not correct, it says "password incorrect"
- if username is present and password is correct, the matching entry from the `users` table is shown

Here is the schema of the `users` table:
```
CREATE TABLE `users` (
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL
);
```

And here is some high-level pseudocode describing the logic:
```
function checkCredentials($link,$usr,$pass){
    $user=mysqli_real_escape_string($link, $usr);
    $password=mysqli_real_escape_string($link, $pass);

    run query "SELECT username from users where username='$user' and password='$password' ";
    if num_rows > 0 return True else False
}

function validUser($link,$usr){
    $user=mysqli_real_escape_string($link, $usr);

    run query $query = "SELECT * from users where username='$user'";
    if num_rows > 0 return True else False
}

function dumpData($link,$usr){
    $user=mysqli_real_escape_string($link, trim($usr));

    run query "SELECT * from users where username='$user'";
    if num_rows > 0 return all the results else False
}

function createUser($link, $usr, $pass){
    if($usr != trim($usr)) {
        echo "Go away hacker";
        return False;
    }
    $user=mysqli_real_escape_string($link, substr($usr, 0, 64));
    $password=mysqli_real_escape_string($link, substr($pass, 0, 64));

    run query "INSERT INTO users (username,password) values ('$user','$password')";
}

if(validUser($link,$_REQUEST["username"])) {
    if(checkCredentials($link,$_REQUEST["username"],$_REQUEST["password"])){
        $data=dumpData($link,$_REQUEST["username"]);
        print htmlentities($data);
    } else {
            echo "Wrong password for user";
    }
} else {
    createUser($link,$_REQUEST["username"],$_REQUEST["password"];
}
```

The important thing to note here is that user input is sanitized with a combination of `trim()`, `subtr()`, and `mysqli_real_escape_string()`. I initially thought the bug would be some way to bypass `mysqli_real_escape_string()`, and indeed found some pages that mention such bypass could be achieved:
- https://shiflett.org/blog/2006/addslashes-versus-mysql-real-escape-string
- https://stackoverflow.com/questions/5741187/sql-injection-that-gets-around-mysql-real-escape-string

However after reading them carefully it only applies to functions `addslashes()` and `mysql_real_escape_string()`.

And I found out the bug actually lies in the inconsistent sanitization between functions in the code. To trigger the bug first submit the form with username such as:
- "natas28                                                              a"

**Note:** the username must start with "natas28", followed by spaces and finally one or more letters. The string must be long enough that `substr($usr, 0, 64)` returns a string consisting of "natas28" followed only be spaces (trailing letters are cut off).

`createUser()` first verifies that `$usr == trim($usr)`; as our input both starts and ends with non-space characters it checks out. Then the username is passed to `substr($usr, 0, 64)`, then the following username is added to the database:
- "natas28                                                         "

Submit the form again, this time using username (both form submissions must use the same password):
- "natas28                                                         "

As neither `validUser()` nor `checkCredentials()` use `trim()` on the input, they both return True. The code then goes to `dumpData()`. That function DOES `trim()` the input, so the query which is run is `SELECT * from users where username='natas28'`. And this way **we get natas28 password**.

Password for the next level is `1JNwQM1Oi6J6j1k49Xyw7ZN6pXMQInVj`.
