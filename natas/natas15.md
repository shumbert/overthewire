Again we can do an SQL injection, however in here we don't see the results. However we can do a blind SQL injection, we make a guess and the page will return 'This user exists' if our guess is true.

First we need to guess the username, lucky us if we try `natas16` it says the user exists. Now we need to guess the password. All natas passwords are 32 characters long, let's use that query to verify the length:
```
natas16" AND LENGTH(password)=32--
```

Server returns 'This user exists' so we are now sure regarding the password length. Now we need to guess character one-by-one, we can use a query like the following:
```
natas16" AND BINARY SUBSTR(password,1,1)="T"-- 
```

We don't want to do that manually so let's write a python script to brute-force the password.

Password for the next level is `hPkjKYviLQctEW33QmuXL6eDVfMW4sGo`.
