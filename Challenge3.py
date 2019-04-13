#/usr/bin/python

import base64
import freqAnalysis

input = bytearray.fromhex('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')

def XORSingleChar(text, key):
	result = b''
		
	for x in text:
		result += bytes([x ^ key])
		
	return result

def XORSingleCharBruteforce(input):
	
	messages = []
	
	for y in range(256):
		result = b''
		
		result = XORSingleChar(input, y)
		messages.append([result, y, freqAnalysis.englishFreqMatchScore(str(result))])
		
	return sorted(messages, key=lambda x: x[2], reverse=True)[0]


print(XORSingleCharBruteforce(input))
