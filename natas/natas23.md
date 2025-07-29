Website has a password text area, we have to provide a string that matches the following conditions:
```
<?php
    if(array_key_exists("passwd",$_REQUEST)){
        if(strstr($_REQUEST["passwd"],"iloveyou") && ($_REQUEST["passwd"] > 10 )){
            echo "<br>The credentials for the next level are:<br>";
            echo "<pre>Username: natas24 Password: <censored></pre>";
        }
        else{
            echo "<br>Wrong!<br>";
        }
    }
    // morla / 10111
?> 
```

First one is easy, our string must include the substring "iloveyou'. The second condition compares our string with the number 10. A quick google search shows that in such case PHP converts the string to a number before comparing the two.

I am not entirely how PHP does that, but it looks like if the string starts with digit characters those will be converted to a number. For instance:
```
11iloveyou -> 11
```

And that's all to it.

Password for the next level is `MeuqmfJ8DDKuTr5pcvzFKSwlxedZYEWd`.
