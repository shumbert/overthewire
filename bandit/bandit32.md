Shell for user bandit32 is a setuid binary, `/home/bandit32/uppershell`. File owner is bandit33 so it should be straight-forward to get the next password. However `uppershell` translates all letters to uppercase before executing the command, so we need some sort of escpape.

I was looking at sh man page, looking for ideas. I was trying the shell special parameters such as $@, $#, ... then I tried:
```
$0
```

This expands to the name of the shell script, which is in the case `sh` (I guess uppershell is a modified version of sh).

So by entering `$0` we launch a new shell which is the regular sh. And now we can finally enter commands.

Password for the next level is `odHo63fHiFqcWWJG9rLiLDtPm45KzUKy`.
