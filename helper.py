import numpy as np

# s - box
sbox = {
	'00' : '63', '01' : '7C', '02' : '77', '03' : '7B', '04' : 'F2', '05' : '6B', 
	'06' : '6F', '07' : 'C5', '08' : '30', '09' : '01', '0A' : '67', '0B' : '2B',
	'0C' : 'FE', '0D' : 'D7', '0E' : 'AB', '0F' : '76',
	'10' : 'CA', '11' : '82', '12' : 'C9', '13' : '7D', '14' : 'FA', '15' : '59',
	'16' : '47', '17' : 'F0', '18' : 'AD', '19' : 'D4', '1A' : 'A2', '1B' : 'AF',
	'1C' : '9C', '1D' : 'A4', '1E' : '72', '1F' : 'C0',
	'20' : 'B7', '21' : 'FD', '22' : '93', '23' : '26', '24' : '36', '25' : '3F',
	'26' : 'F7', '27' : 'CC', '28' : '34', '29' : 'A5', '2A' : 'E5', '2B' : 'F1',
	'2C' : '71', '2D' : 'D8', '2E' : '31', '2F' : '15',
	'30' : '04', '31' : 'C7', '32' : '23', '33' : 'C3', '34' : '18', '35' : '96',
	'36' : '05', '37' : '9A', '38' : '07', '39' : '12', '3A' : '80', '3B' : 'E2',
	'3C' : 'EB', '3D' : '27', '3E' : 'B2', '3F' : '75',
	'40' : '09', '41' : '83', '42' : '2C', '43' : '1A', '44' : '1B', '45' : '6E',
	'46' : '5A', '47' : 'A0', '48' : '52', '49' : '3B', '4A' : 'D6', '4B' : 'B3',
	'4C' : '29', '4D' : 'E3', '4E' : '2F', '4F' : '84',
	'50' : '53', '51' : 'D1', '52' : '00', '53' : 'ED', '54' : '20', '55' : 'FC',
	'56' : 'B1', '57' : '5B', '58' : '6A', '59' : 'CB', '5A' : 'BE', '5B' : '39',
	'5C' : '4A', '5D' : '4C', '5E' : '58', '5F' : 'CF', 
	'60' : 'D0', '61' : 'EF', '62' : 'AA', '63' : 'FB', '64' : '43', '65' : '4D', 
	'66' : '33', '67' : '85', '68' : '45', '69' : 'F9', '6A' : '02', '6B' : '7F', 
	'6C' : '50', '6D' : '3C', '6E' : '9F', '6F' : 'A8', 
	'70' : '51', '71' : 'A3', '72' : '40', '73' : '8F', '74' : '92', '75' : '9D',
	'76' : '38', '77' : 'F5', '78' : 'BC', '79' : 'B6', '7A' : 'DA', '7B' : '21',
	'7C' : '10', '7D' : 'FF', '7E' : 'F3', '7F' : 'D2',
	'80' : 'CD', '81' : '0C', '82' : '13', '83' : 'EC', '84' : '5F', '85' : '97',
	'86' : '44', '87' : '17', '88' : 'C4', '89' : 'A7', '8A' : '7E', '8B' : '3D',
	'8C' : '64', '8D' : '5D', '8E' : '19', '8F' : '73',
	'90' : '60', '91' : '81', '92' : '4F', '93' : 'DC', '94' : '22', '95' : '2A',
	'96' : '90', '97' : '88', '98' : '46', '99' : 'EE', '9A' : 'B8', '9B' : '14',
	'9C' : 'DE', '9D' : '5E', '9E' : '0B', '9F' : 'DB',
	'A0' : 'E0', 'A1' : '32', 'A2' : '3A', 'A3' : '0A', 'A4' : '49', 'A5' : '06',
	'A6' : '24', 'A7' : '5C', 'A8' : 'C2', 'A9' : 'D3', 'AA' : 'AC', 'AB' : '62',
	'AC' : '91', 'AD' : '95', 'AE' : 'E4', 'AF' : '79',
	'B0' : 'E7', 'B1' : 'C8', 'B2' : '37', 'B3' : '6D', 'B4' : '8D', 'B5' : 'D5',
	'B6' : '4E', 'B7' : 'A9', 'B8' : '6C', 'B9' : '56', 'BA' : 'F4', 'BB' : 'EA',
	'BC' : '65', 'BD' : '7A', 'BE' : 'AE', 'BF' : '08',
	'C0' : 'BA', 'C1' : '78', 'C2' : '25', 'C3' : '2E', 'C4' : '1C', 'C5' : 'A6',
	'C6' : 'B4', 'C7' : 'C6', 'C8' : 'E8', 'C9' : 'DD', 'CA' : '74', 'CB' : '1F',
	'CC' : '4B', 'CD' : 'BD', 'CE' : '8B', 'CF' : '8A',
	'D0' : '70', 'D1' : '3E', 'D2' : 'B5', 'D3' : '66', 'D4' : '48', 'D5' : '03',
	'D6' : 'F6', 'D7' : '0E', 'D8' : '61', 'D9' : '35', 'DA' : '57', 'DB' : 'B9',
	'DC' : '86', 'DD' : 'C1', 'DE' : '1D', 'DF' : '9E',
	'E0' : 'E1', 'E1' : 'F8', 'E2' : '98', 'E3' : '11', 'E4' : '69', 'E5' : 'D9',
	'E6' : '8E', 'E7' : '94', 'E8' : '9B', 'E9' : '1E', 'EA' : '87', 'EB' : 'E9',
	'EC' : 'CE', 'ED' : '55', 'EE' : '28', 'EF' : 'DF',
	'F0' : '8C', 'F1' : 'A1', 'F2' : '89', 'F3' : '0D', 'F4' : 'BF', 'F5' : 'E6',
	'F6' : '42', 'F7' : '68', 'F8' : '41', 'F9' : '99', 'FA' : '2D', 'FB' : '0F',
	'FC' : 'B0', 'FD' : '54', 'FE' : 'BB', 'FF' : '16'
}

# input is np array with shape(8,)
def substitute(message):
	row = hex(int(''.join(str(x) for x in message[:4]), 2))[2:]
	col = hex(int(''.join(str(x) for x in message[4:]), 2))[2:]

	res = bin(int(sbox[row + col], 16))[2:].zfill(8)
	return np.array([int(x) for x in res])

# Input for shuffle method must be a numpy array
def shuffle(message, odd=True):
	result = np.zeros((8,8))
	if odd:
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

# input for the shift_bit must be a list
def shift_bit(s, n, direction=1):
	# direction 1 -> right, 0 -> left
	if(direction == 0):
		shifted_part = s[:4*(n-1)]
		main_part = s[4*(n-1):]
		return main_part + shifted_part
	else:
		shifted_part = s[-(4*(n-1)):]
		main_part = s[:-(4*(n-1))]
		return shifted_part + main_part



if __name__ == "__main__":
	# to test something, change False into True
	# test shuffle
	if False:
		a = np.arange(64).reshape((8,8))
		print(a)
		b = shuffle(a, False)
		print('\n', b)

	# test shift bit
	if False:
		c = [i for i in range(64)]
		print('\n', c)
		print('\n', shift_bit(c, 2, direction=0))
		print('\n', shift_bit(c, 2))

	# test sbox substitution
	if False:
		d = np.array([[0,1,1,0,0,0,0,1], [0,1,1,0,0,1,0,1]])
		e = d[0]
		print(substitute(e))