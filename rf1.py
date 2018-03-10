class RF1(object):
	def __init__(self, key_file, filename):
		with open(key_file, 'r') as fin:
			self.key = fin.read()

		with open(filename, 'r') as fin:
			self.plaintext = fin.read()

		# padding bits
		while(len(self.plaintext) % 16 > 0):
			self.plaintext += '0'

if __name__ == "__main__":
	cipher = RF1("key.txt", "input.txt")
	print("key = ", cipher.key)
	print("plaintext = ", cipher.plaintext)