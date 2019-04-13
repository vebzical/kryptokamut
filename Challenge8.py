#/usr/bin/python

import matplotlib.pyplot as plt

input = []

with open('8.txt', 'r') as f:
	for line in f:
		input.append(bytearray.fromhex(line.rstrip()))

for row in input:		
	chunks = [row[i:i+16] for i in range(0, len(row), 16)]
	
	for x in chunks:
		if chunks.count(x) > 1:
			print(row.hex())
			print([i for i,x in enumerate(input) if x == row])
			
