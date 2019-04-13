#/usr/bin/python

import base64

input = bytearray.fromhex('1c0111001f010100061a024b53535009181c')
key = bytearray.fromhex('686974207468652062756c6c277320657965')


def XOR(input, key):
	result = b''

	for x,y in zip(input, key):
		result += bytes([x ^ y])
		
	return result
	
print(XOR(input, key).hex())

