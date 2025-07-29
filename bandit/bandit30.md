Clone the repo using the command:
```
GIT_SSH_COMMAND='ssh -p 2220' git clone ssh://bandit30-git@localhost/home/bandit30-git/repo
```

If you list the remote branches you can the following output:
```
$ GIT_SSH_COMMAND='ssh -p 2220' git ls-remote
From ssh://bandit30-git@localhost/home/bandit30-git/repo
cf552c166d78421e64ddf52f850e680075d216e1	HEAD
cf552c166d78421e64ddf52f850e680075d216e1	refs/heads/master
831aac2e2341f009e40e46392a4f5dd318483019	refs/tags/secret
```

However if you try to checkout the secret tag, you get the following error:
```
$ git checkout tags/secret -b master
fatal: reference is not a tree: tags/secret
```

Looking at the `.git/objects` directory there is a single packfile:
```
$ git verify-pack -v .git/objects/pack/pack-048ed41739bec8a7403d83348801ed06ee5abc92.idx
cf552c166d78421e64ddf52f850e680075d216e1 commit 194 138 12
831aac2e2341f009e40e46392a4f5dd318483019 blob   33 43 150
bd85592e905590f084b8df33363a46f9ac4aa708 tree   37 48 193
029ba421ef4c34205d52133f8da3d69bc1853777 blob   30 38 241
non delta: 4 objects
.git/objects/pack/pack-048ed41739bec8a7403d83348801ed06ee5abc92.pack: ok
```

One blob contains the current `README.md` contents:
```
$ git cat-file -p 029ba421ef4c34205d52133f8da3d69bc1853777
just an epmty file... muahaha
```

But the other contains the juicy stuff:
```
$ git cat-file -p 831aac2e2341f009e40e46392a4f5dd318483019
OoffzGDlzhAlerFJ2cAiz1D41JW1Mhmt
```

Password for the next level is `OoffzGDlzhAlerFJ2cAiz1D41JW1Mhmt`.
