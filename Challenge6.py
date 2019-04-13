#/usr/bin/python

import base64
import freqAnalysis

def XOR(input, key):
	result = b''

	for x,y in zip(input, key):
		result += bytes([x ^ y])
		
	return result

def findKeyLen(chiphertext):
	final_dist = []
	
	for keysize in range(2,41):
		
		distances = []
		
		chunks = [chiphertext[i:i+keysize] for i in range(0, len(chiphertext), keysize)]
		
		for x in range(len(chunks)):
			if x >= (len(chunks)-1):
				break;
			
			one = chunks[x]
			two = chunks[x+1]
			
			distances.append(calcHammingDistance(one,two)/keysize)
			
			chunks.remove(one)
			chunks.remove(two)
			
		final_dist.append([sum(distances)/len(distances), keysize])
		
	sorted_by_second = sorted(final_dist, key=lambda tup: tup[0])
	return sorted_by_second[0][1]
		
	
def calcHammingDistance(str1, str2):
	xord = XOR(str1,str2)
	
	distance = 0
	
	for byte in xord:
		for bit in bin(byte):
			if bit == '1':
				distance += 1
	return distance
	
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
	
def XORRepeatingKey(input, key):
	
	result = b''
	y = 0
	for x in range(len(input)):
		
		if y >= len(key):
			y = 0;

		result += bytes([input[x] ^ key[y]])
		y += 1
		
	return result


input = ""

with open('6.txt', 'r') as f:
	for line in f:
		input += line.rstrip()
		
chiphertext = base64.b64decode(input)
keylen = findKeyLen(chiphertext)

key = b""
plaintexts = []

#Do the Transpose
for i in range(keylen):
	block = b''
	for j in range(i, len(chiphertext), keylen):
		block += bytes([chiphertext[j]])
	key += bytes([XORSingleCharBruteforce(block)[1]])
	result = XORRepeatingKey(chiphertext, key)
	plaintexts.append([result,key,freqAnalysis.englishFreqMatchScore(str(result))])
	
maxscore = max(plaintexts, key=lambda x:x[2])[2]

for i in sorted(plaintexts, key=lambda x: x[2], reverse=True):
	if i[2] == maxscore:
		print(i)
