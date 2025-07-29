ciphertext1 = 'EICTDGYIYZKTHNS'
ciphertext2 = 'PNUKLYLWRQKGKBE'

shifts = []
for i in range(len(ciphertext1)):
    shifts.append((ord(ciphertext1[i]) - ord('A')) % 26)

plaintext = ''
for i in range(len(ciphertext2)):
    plaintext += chr(((ord(ciphertext2[i]) - ord('A') - shifts[i]) % 26) + ord('A'))

print(plaintext)
