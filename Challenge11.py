#/usr/bin/python

import base64
import hashlib
import os
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
	
def encryption_oracle(input):
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
		
def DetectECBMode(ciphertext):
	chunks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
	
	for x in chunks:
		if chunks.count(x) > 1:
			print("ECB")
			return
	print("CBC")

input = b"A"
input = input * 64
DetectECBMode(encryption_oracle(input))



