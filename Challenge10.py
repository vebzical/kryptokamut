#/usr/bin/python

import base64
import hashlib
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
	
def ECBEncrypt(text, key):
	cipher = AES.new(key, AES.MODE_ECB)
	return cipher.encrypt(text)
	
def ECBDecrypt(ciphertext, key)
	decipher = AES.new(key, AES.MODE_ECB)
	return decipher.decrypt(chiphertext)

input = ""
key = b'YELLOW SUBMARINE'

with open('10.txt', 'r') as f:
	for line in f:
		input += line.rstrip()
		
ciphertext = base64.b64decode(input)

blocksize = 16
key = b'YELLOW SUBMARINE'
iv = bytes([0] * 16)

plain = CBCDecrypt(blocksize, ciphertext, AES.new(key, AES.MODE_ECB), iv)
crypted = CBCEncrypt(blocksize, plain, AES.new(key, AES.MODE_ECB), iv)
if crypted == ciphertext:
	print("yay")

