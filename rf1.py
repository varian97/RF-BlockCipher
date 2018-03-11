import numpy as np
import helper

# round function for the feistel network
# all input must be numpy array with shape (8,8)
def round_function(message_L, message_R, internal_key):
	new_L = message_R

	# process the right part of message
	transposed = helper.shuffle(message_R)
	xored = transposed.astype(int) ^ internal_key.astype(int)
	substituted = xored[:,:]
	for i in range(len(xored)):
		substituted[i] = helper.substitute(xored[i])

	print(substituted.dtype)
	new_R = substituted ^ new_L
	return new_L, new_R

class RF1(object):
	def __init__(self, key_file, filename):
		# load the external key
		with open(key_file, 'r') as fin:
			key_temp = fin.read()

		# load the plaintext from file
		with open(filename, 'r') as fin:
			temp = fin.read()

		# padding bits
		while(len(temp) % 16 > 0):
			temp += '0'

		# convert plaintext and key to binary form
		self.plaintext = []
		for i in range(0, len(temp), 16):
			self.plaintext.append(''.join(format(ord(x), '08b') for x in temp[i:i+16]))
		self.key = ''.join(format(ord(x), '08b') for x in key_temp)

	def encrypt(self, nround=16):
		key_L = helper.shift_bit(self.key[:64], 2+1, direction=0)
		key_R = helper.shift_bit(self.key[64:], 2+1)
		ciphertext = ""

		for message in self.plaintext:
			# generate message matrix
			message_L = np.array([int(x) for x in message[:64]]).reshape((8,8))
			message_R = np.array([int(x) for x in message[64:]]).reshape((8,8))

			for iteration in range(nround):
				# generate internal keys
				key_L = helper.shift_bit(self.key[:64], iteration+1, direction=0)
				key_R = helper.shift_bit(self.key[64:], iteration+1)
				internal_key = np.array([int(i) ^ int(j) for i,j in zip(key_L, key_R)]).reshape((8,8))

				message_L, message_R = round_function(message_L, message_R, internal_key)

			# combine the message again
			combined = np.append(message_L.reshape((64,)), message_R.reshape((64,)))
			combined = ''.join(str(x) for x in combined)
			for i in range(0,len(combined),8):
				ciphertext += chr(int(combined[i:i+8], 2))

		return ciphertext

if __name__ == "__main__":
	cipher = RF1("key.txt", "input.txt")
	print(cipher.encrypt())