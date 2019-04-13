#/usr/bin/python

import base64
import freqAnalysis


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

results = []
with open('4.txt', 'r') as f:
	for line in f:
		results.append(XORSingleCharBruteforce(bytearray.fromhex(line.rstrip())))
		
maxscore = max(results, key=lambda x:x[2])[2]

for i in sorted(results, key=lambda x: x[2], reverse=True):
	if i[2] == maxscore:
		print(i)




