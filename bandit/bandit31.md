Clone the repo using the command:
```
GIT_SSH_COMMAND='ssh -p 2220' git clone ssh://bandit31-git@localhost/home/bandit31-git/repo
```

The README.md file tells you to push a file to the remote repository so just do it:
```
vim .gitignore # .gitignore is set to ignore txt file, so comment out the line first
git add key.txt
git commit -m 'commit'
GIT_SSH_COMMAND='ssh -p 2220' git push
```

Password for the next level is `rmCBvG56y58BXzv98yZGdO7ATVL5dW8y`.
