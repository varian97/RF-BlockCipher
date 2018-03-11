def shuffle(message, odd=True):
	result = np.zeros((8,8))
	if odd == True:
		# clockwise rotation the outer layer
		result[0, 1:] = message[0, :-1]
		result[1:, 7] = message[:-1, 7]
		result[7, :-1] = message[7, 1:]
		result[:-1, 0] = message[1:, 0]

		#counter clockwise rotation the outer layer - 1
		result[1, 1:6] = message[1, 2:7]
		result[2:7, 1] = message[1:6, 1]
		result[6, 2:7] = message[6, 1:6]
		result[1:6, 6] = message[2:7, 6]

		#clockwise rotation the outer layer - 2
		result[2, 3:6] = message[2, 2:5]
		result[3:6, 5] = message[2:5, 5]
		result[5, 2:5] = message[5, 3:6]
		result[2:5, 2] = message[3:6, 2]

		#counter clockwise rotation the inner layer
		result[3,3] = message[3,4]
		result[4,3] = message[3,3]
		result[4,4] = message[4,3]
		result[3,4] = message[4,4]
	else:
		#counter clockwise rotation the outer layer
		result[0, :-1] = message[0, 1:]
		result[1:, 0] = message[0:-1, 0]
		result[7, 1:] = message[7, :-1]
		result[:-1, 7] = message[1:, 7]

		# clockwise rotation the outer layer - 1
		result[1, 2:7] = message[1, 1:6]
		result[2:7, 6] = message[1:6, 6]
		result[6, 1:6] = message[6, 2:7]
		result[1:6, 1] = message[2:7, 1]

		# counter clockwise rotation the outer layer - 2
		result[2, 2:5] = message[2, 3:6]
		result[3:6, 2] = message[2:5, 2]
		result[5, 3:6] = message[5, 2:5]
		result[2:5, 5] = message[3:6, 5]

		#clockwise rotation the inner layer
		result[3,3] = message[4,3]
		result[3,4] = message[3,3]
		result[4,4] = message[3,4]
		result[4,3] = message[4,4]

	return result


if __name__ == "__main__":
	import numpy as np

	a = np.arange(64).reshape((8,8))
	print(a)
	b = shuffle(a, False)
	print('\n', b)