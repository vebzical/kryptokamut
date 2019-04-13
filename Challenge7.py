#/usr/bin/python

import base64
from Crypto.Cipher import AES

input = ""
key = b'YELLOW SUBMARINE'

with open('7.txt', 'r') as f:
	for line in f:
		input += line.rstrip()
		
chiphertext = base64.b64decode(input)

decipher = AES.new(key, AES.MODE_ECB)
print(decipher.decrypt(chiphertext))
