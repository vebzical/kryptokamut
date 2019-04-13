#/usr/bin/python

import base64
import hashlib
import os
import random
from random import randint
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor


def CBCEncrypt(blocksize, text, ECB, iv):
	text = PKCS7Pad(blocksize, text)
	PKCS7Pad(blocksize, text)
	blocks = [text[i:i+blocksize] for i in range(0, len(text), blocksize)]
	prev = iv
	encrypted = b''
	for block in blocks:
		encryptedblock = ECB.encrypt(strxor(block, prev))
		prev = encryptedblock
		encrypted += encryptedblock
	return encrypted

def CBCDecrypt(blocksize, ciphertext, ECB, iv):
	blocks = [ciphertext[i:i+blocksize] for i in range(0, len(ciphertext), blocksize)]
	prev = iv
	decrypted = b""
	for block in blocks:
		decryptedblock = strxor(prev, ECB.decrypt(block))
		prev  = block
		decrypted += decryptedblock
	return decrypted

def PKCS7Pad(blocksize, text):
	paddingchar = b"\x00"
	requiredpad = (blocksize - len(text) % blocksize)
	if requiredpad != blocksize:
		text += (paddingchar * requiredpad)
	return text
	
def ECBEncrypt(text, key, blocksize):
	text = PKCS7Pad(blocksize, text)
	cipher = AES.new(key, AES.MODE_ECB)
	return cipher.encrypt(text)
	
def ECBDecrypt(ciphertext, key):
	decipher = AES.new(key, AES.MODE_ECB)
	return decipher.decrypt(chiphertext)
	
def GenerateRandomKey():
	return Random.new().read(16)
	
def GenerateRandomIV():
	return Random.new().read(16)
	
def Encryption_oracle(input, ):
	blocksize = 16
	key = GenerateRandomKey()
	iv = GenerateRandomIV()
	plain = Random.new().read(randint(5, 10)) + input + Random.new().read(randint(5, 10))

	if randint(0, 1) == 0:
		print("Did CBC")
		return CBCEncrypt(blocksize, plain, AES.new(key, AES.MODE_ECB), iv)		
	else:
		print("Did ECB")
		return ECBEncrypt(plain, key, blocksize)
		
def EncryptionOracleECB(input, key):
	blocksize = 16
	iv = GenerateRandomIV()
	plain = input

	return ECBEncrypt(plain, key, blocksize)
		
def DetectECBMode(ciphertext):
	chunks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
	
	for x in chunks:
		if chunks.count(x) > 1:
			return "ECB"			
	return "CBC"
	
def DetectBlockSize(text, randomprefix, key):
	aaa = b"A"
	prev = EncryptionOracleECB(text, key)
	
	for i in range(64):
		payload = randomprefix+(aaa * i)+text
		result = EncryptionOracleECB(payload, key)
		if len(prev) != len(result):
			return len(result) - len(prev)
		prev = result
		
def DetectSecretSize(text, randomprefix, key):
	aaa = b"A"
	prev = EncryptionOracleECB(text, key)
	
	for i in range(128):
		payload = randomprefix+(aaa * i)+text
		result = EncryptionOracleECB(payload, key)
		if len(prev) != len(result):
			return len(prev) - i
		prev = result

def BruteforceECB(ciphersize, blocksize, value, randomprefix, prefixsize, key):
	plain = b""
	startpad = (blocksize - prefixsize) * b'A'
	
	for x in range(ciphersize):

		aaa = b"A" * (blocksize - (len(plain) % blocksize) - 1)
		aaa = startpad + aaa
		compare = EncryptionOracleECB(randomprefix + aaa + value, key)[:len(aaa) + len(plain) + 1]
		
		for i in range(256):
			test = aaa + plain + bytes([i])
			result = EncryptionOracleECB(randomprefix + test + value, key)[:len(aaa) + len(plain) + 1]
			if compare == result:
				plain += bytes([i])
				print(chr(i))
				break

	return plain
	
def determinePrefixLength(blocksize, value, randomprefix, key):

	for y in range(blocksize*5):	
		payload = (b"A"*y)
		ciphertext = EncryptionOracleECB(randomprefix+payload+value, key)
		chunks = [ciphertext[i:i+blocksize] for i in range(0, len(ciphertext), blocksize)]
		
		for x in chunks:
			if chunks.count(x) > 1:
				return blocksize - (y - (blocksize * 2))
				
value = base64.b64decode("Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK")
key = GenerateRandomKey()
randomprefix = Random.new().read(random.randint(1,16))

blocksize = DetectBlockSize(value, randomprefix, key)
mode = DetectECBMode(EncryptionOracleECB((randomprefix + (b"A" * blocksize * 3) + value), key))
ciphersize = DetectSecretSize(value, randomprefix, key)
prefixsize  = determinePrefixLength(blocksize, value, randomprefix, key)

print(BruteforceECB(ciphersize, blocksize, value, randomprefix, prefixsize, key))
