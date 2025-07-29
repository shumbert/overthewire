Again we have the server-side code.

Page is a login form, analysis of the server-side code shows a classic SQL injection. Code performs an SQL query:
```
   $query = "SELECT * from users where username=\"".$_REQUEST["username"]."\" and password=\"".$_REQUEST["password"]."\"";
```

And returns the next level password if the query returned at least one result. We can trick the code logic by using:
- username: `bob
- password; `foobar" OR 1=1-- `

Password for next level is `SdqIqBsFcz3yotlNYErZSZwblkm0lrvx`.
