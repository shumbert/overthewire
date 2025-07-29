# Overview
Home directory has a setuid binary `leviathan6`, owned by leviathan7. When run it says:
```
leviathan6@gibson:~$ ./leviathan6
usage: ./leviathan6 <4 digit code>
leviathan6@gibson:~$ ./leviathan6 1234
Wrong
```

# Reversing
Not much happening here, `main` is the only function of interest. It compares the argument with the static value 0x1bd3. It it's the same it runs `/bin/sh` via system(). So you just have to run the binary using `./leviathan6 7123`.

Password for next level is `qEs5Io5yM8`.
