#/usr/bin/python

import base64
import hashlib
import os
import random
import urllib
from random import randint
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
from urllib.parse import quote_from_bytes


class PaddingError(Exception):
   """Raised when the input value is too small"""
   pass

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
	requiredpad = (blocksize - len(text) % blocksize)
	paddingchar = bytes([requiredpad])
	
	if requiredpad != blocksize:
		text += (paddingchar * requiredpad)
	return text
	
def PKCS7Strip(text, blocksize):
	
	if not len(text) % blocksize == 0:
		print("Wrong block size")
		raise PaddingError
	
	if not PKCS7Check(text):
		return text
	
	last_byte = text[-1]
	padding_size = int(last_byte)
		
	if not text.endswith(bytes([last_byte])*padding_size):
		print("Wrong bytes")
		raise PaddingError
	
	return text[:-padding_size]
	

def PKCS7Check(binary_data):
	# Take what we expect to be the padding
    padding = binary_data[-binary_data[-1]:]
    # Check that all the bytes in the range indicated by the padding are equal to the padding value itself
    return all(padding[b] == len(padding) for b in range(0, len(padding)))
	
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
	
def Encryption_oracle(input):
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
				#print(chr(i))
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
				
def EncryptMessage(key, msg):
	#print([msg[i:i+16] for i in range(0, len(msg), 16)])
	iv = GenerateRandomIV()
	msg = PKCS7Pad(16, msg)
	ciphertext = CBCEncrypt(16, msg, AES.new(key, AES.MODE_ECB), iv)
	
	return {"iv":iv, "ciphertext":ciphertext}

def decrypt_and_check_padding(key, ctxt):
	ptxt = CBCDecrypt(16, ctxt["ciphertext"], AES.new(key, AES.MODE_ECB), ctxt["iv"])
	print(ptxt)
	try:
		txt = PKCS7Strip(ptxt, 16)
	except:
		return False 
	return True

key = GenerateRandomKey()
	
with open('17.txt', 'r') as f:
	for line in f:
		input = line.rstrip()
		ctxt = EncryptMessage(key, base64.b64decode(input))
		print(decrypt_and_check_padding(key, ctxt))
