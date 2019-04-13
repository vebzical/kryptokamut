key = b'YELLOW SUBMARINE'


def PKCS7Pad(input, length):
	if len(input) < length:
		need =  length - len(input)
		for i in range(need):
			input += b"\x04"
	return input
	
print(PKCS7Pad(key,20))
			
