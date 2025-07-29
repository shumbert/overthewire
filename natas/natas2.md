There is nothing on the page so I ran gobuster:
```
gobuster dir -u http://natas2.natas.labs.overthewire.org/ -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -U natas2 -P h4ubbcXrWqsTo7GGnnUMLppXbOogfBZ7 -z
```

Gobuster found a /files folder, I browsed to the folder and there was a users.txt file with a bunch of credentials, including the one for natas3.

Password for next level is `3gqisGdR0pjm6tpkDKdIWO2hSvchLeYH`.
