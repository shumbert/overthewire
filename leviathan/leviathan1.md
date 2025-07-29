Home directory has a setuid binary `check`, owned by leviathan2. When run it prompts for a password.

Initially I used `strings` to look for interesting strings, but no luck. So I ended up debugging it with gdb and found out the password is `sex`. By default `strings` looks for strings 4 characters or longer, I should have used `strings -n 3 check`.

After entering the password I get a shell as leviathan2 and read the password from `/etc/leviathan_pass/leviathan_pass2`.

Password for the next level is `NsN1HwFoyN`.
