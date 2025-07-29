Source code for the page is available, with the following PHP code:
```
<?php

/*
CREATE TABLE `users` (
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL
);
*/

if(array_key_exists("username", $_REQUEST)) {
    $link = mysqli_connect('localhost', 'natas17', '<censored>');
    mysqli_select_db($link, 'natas17');

    $query = "SELECT * from users where username=\"".$_REQUEST["username"]."\"";
    if(array_key_exists("debug", $_GET)) {
        echo "Executing query: $query<br>";
    }

    $res = mysqli_query($link, $query);
    if($res) {
    if(mysqli_num_rows($res) > 0) {
        //echo "This user exists.<br>";
    } else {
        //echo "This user doesn't exist.<br>";
    }
    } else {
        //echo "Error in query.<br>";
    }
...    
```

So it looks like we can perform an SQL injection using the `username` request parameter. We can't see the query results, however we can perform a blind SQL injection.

So I have a first script to brute-force usernames, it finds the following usernames:
- natas18
- user1
- user2
- user3

Then there is another script to brute-force natas18 password.

Password for the next level is `6OG1PbKdVjyBlpxgD4DDbRG6ZLlCGgCJ`.
