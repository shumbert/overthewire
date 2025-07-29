First thing when logging in as bandit25 we can see an sshkey in /home/bandit25/bandit26.sshkey.

So we can ssh as bandit26, however that user shell is /usr/bin/showtext:
```
#!/bin/sh

export TERM=linux

exec more ~/text.txt
exit 0
```

/home/bandit26/text.txt just contains:
```
  _                     _ _ _   ___   __  
 | |                   | (_) | |__ \ / /  
 | |__   __ _ _ __   __| |_| |_   ) / /_  
 | '_ \ / _` | '_ \ / _` | | __| / / '_ \ 
 | |_) | (_| | | | | (_| | | |_ / /| (_) |
 |_.__/ \__,_|_| |_|\__,_|_|\__|____\___/ 
```

So the idea would be to use more subshell feature, however when ssh-ing more returns directly so no luck.

The trick here is to resize the terminal window to force more to page through the file. Once you done that type `v` to switch to vi then enter the command `:e /etc/bandit_pass/bandit26` to see the password.

Password for level 26 is `c7GvcKlw9mC7aUQaPx7nwFstuAIBw1o1`.
