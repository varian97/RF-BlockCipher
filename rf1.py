import numpy as np
import helper

# round function for the feistel network
# all input must be numpy array with shape (8,8)
def round_function(message_L, message_R, internal_key, iteration):
	new_L = message_R

	# process the right part of message
	if iteration % 2 == 0:
		transposed = helper.shuffle(message_R, False)
	else:
		transposed = helper.shuffle(message_R)

	dotted = np.remainder(np.dot(transposed, internal_key), 2).astype(int)
	substituted = dotted[:,:]
	for i in range(len(dotted)):
		substituted[i] = helper.substitute(dotted[i])

	new_R = substituted ^ message_L
	return new_L, new_R

def round_function_inverse(message_L, message_R, internal_key, iteration):
	new_R = message_L

	# process the right part of message
	if iteration % 2 == 0:
		transposed = helper.shuffle(message_L, False)
	else:
		transposed = helper.shuffle(message_L)

	dotted = np.remainder(np.dot(transposed, internal_key), 2).astype(int)
	substituted = dotted[:,:]
	for i in range(len(dotted)):
		substituted[i] = helper.substitute(dotted[i])

	new_L = substituted ^ message_R
	return new_L, new_R

class RF1(object):
	def __init__(self, key_file, filename, iv_file):
		# load the external key
		with open(key_file, 'r') as fin:
			key_temp = fin.read()

		# load the plaintext from file
		with open(filename, 'r') as fin:
			temp = fin.read()

      # load the plaintext from file
		with open(iv_file, 'r') as fin:
			iv_temp = fin.read()

		# padding bits
		while(len(temp) % 16 > 0):
			temp += '0'

		# convert plaintext and key to binary form
		self.plaintext = []
		for i in range(0, len(temp), 16):
			self.plaintext.append(''.join(format(ord(x), '08b') for x in temp[i:i+16]))
			self.key = ''.join(format(ord(x), '08b') for x in key_temp)
			self.iv = ''.join(format(ord(x), '08b') for x in iv_temp)

	# ecb is the default for the encryption
	def encrypt_ecb_cbc(self, nround=16, mode='ecb'):
		if(mode == 'cbc'):
			previous_encrypted_message = self.iv

		ciphertext = ""

		for message in self.plaintext:
			if(mode == 'cbc'):
				if len(previous_encrypted_message) > 0:
					message = ''.join(str(int(i) ^ int(j)) for i, j in zip(message, previous_encrypted_message))

			# generate message matrix
			message_L = np.array([int(x) for x in message[:64]]).reshape((8,8))
			message_R = np.array([int(x) for x in message[64:]]).reshape((8,8))

			for iteration in range(nround):
				# generate internal keys
				key_L = helper.shift_bit(self.key[:64], iteration+1, direction=0)
				key_R = helper.shift_bit(self.key[64:], iteration+1)
				internal_key = np.array([int(i) ^ int(j) for i,j in zip(key_L, key_R)]).reshape((8,8))

				message_L, message_R = round_function(message_L, message_R, internal_key, iteration+1)

			# combine the message again
			combined = np.append(message_L.reshape((64,)), message_R.reshape((64,)))
			combined = ''.join(str(x) for x in combined)

			# if the mode is cbc, store the current result for the next message
			if(mode == 'cbc'):
				previous_encrypted_message = combined

			for i in range(0,len(combined),8):
				ciphertext += chr(int(combined[i:i+8], 2))

		return ciphertext

	# ecb is the default for decryption
	def decrypt_ecb_cbc(self, ciphertext, nround=16, mode='ecb'):
		if(mode == 'cbc'):
			previous_encrypted_message = []
			previous_encrypted_message.append(self.iv)

		plaintext = ""

		# convert ciphertext to binary form
		temp_cipher = []
		for i in range(0, len(ciphertext), 16):
			temp_cipher.append(''.join(format(ord(x), '08b') for x in ciphertext[i:i+16]))

		for index, message in enumerate(temp_cipher):
			# if mode is cbc, we must store the current ciphertext for decoding the next block of message
			if(mode == 'cbc'):
				previous_encrypted_message.append(message)

			# generate message matrix
			message_L = np.array([int(x) for x in message[:64]]).reshape((8,8))
			message_R = np.array([int(x) for x in message[64:]]).reshape((8,8))

			for iteration in reversed(range(nround)):
				# generate internal keys
				key_L = helper.shift_bit(self.key[:64], iteration+1, direction=0)
				key_R = helper.shift_bit(self.key[64:], iteration+1)
				internal_key = np.array([int(i) ^ int(j) for i,j in zip(key_L, key_R)]).reshape((8,8))

				message_L, message_R = round_function_inverse(message_L, message_R, internal_key, iteration+1)		

			# combine the message again
			combined = np.append(message_L.reshape((64,)), message_R.reshape((64,)))
			combined = ''.join(str(x) for x in combined)

			# if the mode is cbc, we must convert the plaintext to the actual plaintext
			if(mode == 'cbc'):
				combined = ''.join(str(int(i) ^ int(j)) for i,j in zip(combined, previous_encrypted_message[-2]))

			for i in range(0,len(combined),8):
				plaintext += chr(int(combined[i:i+8], 2))

		return plaintext		

	def encrypt_CFB(self, nround=16):
		iv = self.iv
		ciphertext = ""
        
		for message in self.plaintext:
			# generate iv matrix
			iv_L = np.array([int(x) for x in iv[:64]]).reshape((8,8))
			iv_R = np.array([int(x) for x in iv[64:]]).reshape((8,8))

			for iteration in range(nround):
				# generate internal keys
				key_L = helper.shift_bit(self.key[:64], iteration+1, direction=0)
				key_R = helper.shift_bit(self.key[64:], iteration+1)
				internal_key = np.array([int(i) ^ int(j) for i,j in zip(key_L, key_R)]).reshape((8,8))
    
				iv_L, iv_R = round_function(iv_L, iv_R, internal_key, iteration+1)

			# combine the message again
			combined = np.append(iv_L.reshape((64,)), iv_R.reshape((64,)))
			combined = ''.join(str(x) for x in combined)

			iv = ''.join(str(int(i) ^ int(j)) for i, j in zip(message, combined))

			for i in range(0,len(iv),8):
				ciphertext += chr(int(iv[i:i+8], 2))
                
		return ciphertext
    
	def decrypt_CFB(self, ciphertext, nround=16):
		iv = self.iv
		plaintext = ""
        
		# convert ciphertext to binary form
		temp_cipher = []
		for i in range(0, len(ciphertext), 16):
			temp_cipher.append(''.join(format(ord(x), '08b') for x in ciphertext[i:i+16]))
        
		for index, message in enumerate(temp_cipher):
			# generate iv matrix
			iv_L = np.array([int(x) for x in iv[:64]]).reshape((8,8))
			iv_R = np.array([int(x) for x in iv[64:]]).reshape((8,8))
            
			for iteration in range(nround):
				# generate internal keys
				key_L = helper.shift_bit(self.key[:64], iteration+1, direction=0)
				key_R = helper.shift_bit(self.key[64:], iteration+1)
				internal_key = np.array([int(i) ^ int(j) for i,j in zip(key_L, key_R)]).reshape((8,8))
                    
				iv_L, iv_R = round_function(iv_L, iv_R, internal_key, iteration+1)
                
			# combine the message again
			combined = np.append(iv_L.reshape((64,)), iv_R.reshape((64,)))
			combined = ''.join(str(x) for x in combined)
            
			iv = message
            
			temp_plain = ''.join(str(int(i) ^ int(j)) for i, j in zip(message, combined))
            
			for i in range(0,len(temp_plain),8):
				plaintext += chr(int(temp_plain[i:i+8], 2))
                
		return plaintext

	# wrapper function for encryption
	def encrypt(self, nround=16, mode='ecb'):
		if(mode == 'ecb'):
			return self.encrypt_ecb_cbc(nround=nround)
		elif(mode == 'cbc'):
			return self.encrypt_ecb_cbc(nround=nround, mode='cbc')
		elif(mode == 'cfb'):
			return self.encrypt_CFB(nround=nround)

	# wrapper function for decryption
	def decrypt(self, ciphertext, nround=16, mode='ecb'):
		if(mode == 'ecb'):
			return self.decrypt_ecb_cbc(ciphertext=ciphertext, nround=nround)
		elif(mode == 'cbc'):
			return self.decrypt_ecb_cbc(ciphertext=ciphertext, nround=nround, mode='cbc')
		elif(mode == 'cfb'):
			return self.decrypt_CFB(ciphertext=ciphertext, nround=nround)

if __name__ == "__main__":
	cipher = RF1("key.txt", "input.txt", "iv.txt")
	encrypted = cipher.encrypt(mode='cfb')
	print("Encrypt = ", encrypted)
	decrypted = cipher.decrypt(encrypted, mode='cfb')
	print("Decrypt = ",decrypted)