#/usr/bin/python

import base64

input1 = bytearray(b"Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal")
input2 = bytearray(b"")
key = bytearray(b"ICE")

def XORRepeatingKey(input):
	
	result = b''
	y = 0
	for x in range(len(input)):
		
		if y >= len(key):
			y = 0;

		result += bytes([input[x] ^ key[y]])
		y += 1
		
	return result


print(XORRepeatingKey(input1).hex())
