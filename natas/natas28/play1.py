#! /usr/bin/env python3

import sys
import urllib.error
import urllib.parse
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def send_request(url, headers, data):
    req = urllib.request.Request(url=url, data=data.encode(), headers=headers)
    try:
        r = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        r = e

    encoded_blob = r.headers['Location'].replace('search.php/?query=', '')
    return urllib.parse.unquote(encoded_blob)


def main():
    opener = urllib.request.build_opener(NoRedirect)
    urllib.request.install_opener(opener)

    url = 'http://natas28.natas.labs.overthewire.org/index.php'
    headers = {
        'Authorization': 'Basic bmF0YXMyODpza3J3eGNpQWU2RG5iMFZmRkR6REVIY0N6UW12M0dkNA=='
    }

    for i in range(33):
        data = 'query=' + urllib.parse.quote("A" * i)
        encrypted_blob = send_request(url, headers, data)
        print(f'{i:02} chars: {encrypted_blob}')


if __name__ == '__main__':
    main()
