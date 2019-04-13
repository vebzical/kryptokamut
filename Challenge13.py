#/usr/bin/python

import base64
import hashlib
import os
import random
from random import randint
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor



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
	return decipher.decrypt(ciphertext)
	
def GenerateRandomKey():
	return Random.new().read(16)
	
def GenerateRandomIV():
	return Random.new().read(16)
		
def EncryptionOracleECB(input, key):
	blocksize = 16
	iv = GenerateRandomIV()
	
	return ECBEncrypt(input, key, blocksize)
	
def parse(byte_string):
	string = byte_string.decode()
	result = dict(pair.split('=')
				  for pair in string.split('&'))
	return result

def profile_for(email):
	if b"&" in email or b"=" in email:
		raise ValueError("Invalid email address")
	return b"email=" + email + b'&uid=10&role=user'

def get_encrypted_profile(email, key):
	profile = profile_for(email)
	return EncryptionOracleECB(profile, key)

def decrypt_and_parse_profile(key, ctxt):
	profile = ECBDecrypt(ctxt, key)
	return parse(profile)
	
#Static key used
key = b"kissakissakissak"

#Value to generate admin block
value = b"kissakissakissakissakissaAadmin" + b"\00" * 11

encr = EncryptionOracleECB(profile_for(value), key)
text = ECBDecrypt(encr, key)
chunks = [text[i:i+16] for i in range(0, len(text), 16)]
print(chunks)
##Save the admin block
chunks = [encr[i:i+16] for i in range(0, len(encr), 16)]
adminblock = chunks[2]

# Create encrypted text so role value is in a new block
value = b"kiss@koira.fi"

encr = EncryptionOracleECB(profile_for(value), key)
text = ECBDecrypt(encr, key)
chunks = [encr[i:i+16] for i in range(0, len(encr), 16)]
print(chunks)

#Save all except for the role value
payload = encr[:32]
payload += adminblock

print(payload)
text = ECBDecrypt(payload, key)

profile = parse(text)
print(profile)
print(profile["role"])

