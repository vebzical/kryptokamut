#/usr/bin/python

import matplotlib.pyplot as plt

input = bytearray.fromhex('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
print(input.hex())

plt.hist(input)
plt.xticks(range(0, 256, 10))
plt.show()


