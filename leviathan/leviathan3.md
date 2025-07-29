# Setuid binary
Home directory has a setuid binary `level3`, owned by leviathan4. It expects a password as argument:
```
leviathan3@gibson:~$ ./level3
Enter the password> foo
bzzzzzzzzap. WRONG
leviathan3@gibson:~$
```

# Figuring out the secret password
It was easier than expected, the binary has two functions `main()` and `do_stuff()`. `do_stuff()` compares the secret password with the password entered by the user, so it's just matter of debugging the binary and printing the secret password.

I guess the trick is that the password is not stored in the binary global section, but instead built in the stack using immediate value:
```
   0x080491eb <+21>:	mov    DWORD PTR [ebp-0x117],0x706c6e73 ; copies "snlp"
   0x080491f5 <+31>:	mov    DWORD PTR [ebp-0x113],0x746e6972 ; copies "rint"
   0x080491ff <+41>:	mov    DWORD PTR [ebp-0x110],0xa6674    ; copies "tf\n\0" (note that the 't' byte is overwritten here)
                                                                ; note that the null-byte is kind of transparent here
                                                                ; however the value copied to the stack is 0x000a6674
                                                                ; so the string is null-byte terminated
```

Password for the next level is `WG1egElCvO`.
