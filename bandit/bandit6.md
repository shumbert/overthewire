Similar as the previous one, we have to use find to find a file:
> owned by user bandit7
    owned by group bandit6
    33 bytes in size

Use:
```
find / -user bandit7 -group bandit6 -size 33c
```
