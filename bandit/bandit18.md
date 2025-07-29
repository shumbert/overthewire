We just get `Byebye !` when SSH-ing to the box as someone modified .bashrc.

However we can read the password from the readme file by using this command to SSH:
```
ssh bandit.labs.overthewire.org -p 2220 -l bandit18 cat readme
```

Password for level 19 is `awhqfNnAbc1naukrpqDYcF95h7HoMTrC`.
