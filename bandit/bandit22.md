`/etc/cron.d/cronjob_bandit23` runs script `/usr/bin/cronjob_bandit23.sh`.

The shell script generates a MD5 hash and copy the next level password to `/tmp/<hash>`. To find out the hash just run:
```
echo I am user bandit23 | md5sum | cut -d ' ' -f 1
```

Then cat file `/tmp/8ca319486bfbbc3663ea0fbe81326349`.

Password for the next level is `QYw0Y2aiA672PsMmh9puTQuhoz8SyR2G`.
