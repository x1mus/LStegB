def is_prime(num):
	"""Check if the number in paramter is a prime number, return True if it's the case, return False otherwise
	"""
	return all(num % i for i in range(2, num))

def parity_bit(num):
	binary = bin(num).replace("0b", "")
	count = str(binary).count('1')

	return True if count % 2 == 0 else False

def la_to_binary(bits_quantity, channel, l, a=None):
	l_binary = '{0:08b}'.format(l)

	if a is not None:
		a_binary = '{0:08b}'.format(a)

	if channel == "LA":
		return l_binary[-bits_quantity:] + a_binary[-bits_quantity:]
	elif channel == "AL":
		return a_binary[-bits_quantity:] + l_binary[-bits_quantity:]
	elif channel == "L":
		return l_binary[-bits_quantity:]
	elif channel == "A":
		return a_binary[-bits_quantity:]

def rgba_to_binary(bits_quantity, channel, r, g, b, a=None):
	r_binary = '{0:08b}'.format(r)
	g_binary = '{0:08b}'.format(g)
	b_binary = '{0:08b}'.format(b)	
	
	if a is not None:
		a_binary = '{0:08b}'.format(a)

	if channel == "RGBA":
		return r_binary[-bits_quantity:] + g_binary[-bits_quantity:] + b_binary[-bits_quantity:] + a_binary[-bits_quantity:]
	elif channel == "RGAB":
		return r_binary[-bits_quantity:] + g_binary[-bits_quantity:] + a_binary[-bits_quantity:] + b_binary[-bits_quantity:]
	elif channel == "RAGB":
		return r_binary[-bits_quantity:] + a_binary[-bits_quantity:] + g_binary[-bits_quantity:] + b_binary[-bits_quantity:]
	elif channel == "RABG":
		return r_binary[-bits_quantity:] + a_binary[-bits_quantity:] + b_binary[-bits_quantity:] + g_binary[-bits_quantity:]
	elif channel == "RBGA":
		return r_binary[-bits_quantity:] + b_binary[-bits_quantity:] + g_binary[-bits_quantity:] + a_binary[-bits_quantity:]
	elif channel == "RBAG":
		return r_binary[-bits_quantity:] + b_binary[-bits_quantity:] + a_binary[-bits_quantity:] + g_binary[-bits_quantity:]
	elif channel == "BGRA":
		return b_binary[-bits_quantity:] + g_binary[-bits_quantity:] + r_binary[-bits_quantity:] + a_binary[-bits_quantity:]
	elif channel == "BGAR":
		return b_binary[-bits_quantity:] + g_binary[-bits_quantity:] + a_binary[-bits_quantity:] + r_binary[-bits_quantity:]
	elif channel == "BAGR":
		return b_binary[-bits_quantity:] + a_binary[-bits_quantity:] + g_binary[-bits_quantity:] + r_binary[-bits_quantity:]
	elif channel == "BARG":
		return b_binary[-bits_quantity:] + a_binary[-bits_quantity:] + r_binary[-bits_quantity:] + g_binary[-bits_quantity:]
	elif channel == "BRGA":
		return b_binary[-bits_quantity:] + r_binary[-bits_quantity:] + g_binary[-bits_quantity:] + a_binary[-bits_quantity:]
	elif channel == "BRAG":
		return b_binary[-bits_quantity:] + r_binary[-bits_quantity:] + a_binary[-bits_quantity:] + g_binary[-bits_quantity:]
	elif channel == "GRBA":
		return g_binary[-bits_quantity:] + r_binary[-bits_quantity:] + b_binary[-bits_quantity:] + a_binary[-bits_quantity:]
	elif channel == "GRAB":
		return g_binary[-bits_quantity:] + r_binary[-bits_quantity:] + a_binary[-bits_quantity:] + b_binary[-bits_quantity:]
	elif channel == "GARB":
		return g_binary[-bits_quantity:] + a_binary[-bits_quantity:] + r_binary[-bits_quantity:] + b_binary[-bits_quantity:]
	elif channel == "GABR":
		return g_binary[-bits_quantity:] + a_binary[-bits_quantity:] + b_binary[-bits_quantity:] + r_binary[-bits_quantity:]
	elif channel == "GBRA":
		return g_binary[-bits_quantity:] + b_binary[-bits_quantity:] + r_binary[-bits_quantity:] + a_binary[-bits_quantity:]
	elif channel == "GBAR":
		return g_binary[-bits_quantity:] + b_binary[-bits_quantity:] + a_binary[-bits_quantity:] + r_binary[-bits_quantity:]
	elif channel == "AGBR":
		return a_binary[-bits_quantity:] + g_binary[-bits_quantity:] + b_binary[-bits_quantity:] + r_binary[-bits_quantity:]
	elif channel == "AGRB":
		return a_binary[-bits_quantity:] + g_binary[-bits_quantity:] + r_binary[-bits_quantity:] + b_binary[-bits_quantity:]
	elif channel == "ARGB":
		return a_binary[-bits_quantity:] + r_binary[-bits_quantity:] + g_binary[-bits_quantity:] + b_binary[-bits_quantity:]
	elif channel == "ARBG":
		return a_binary[-bits_quantity:] + r_binary[-bits_quantity:] + b_binary[-bits_quantity:] + g_binary[-bits_quantity:]
	elif channel == "ABGR":
		return a_binary[-bits_quantity:] + b_binary[-bits_quantity:] + g_binary[-bits_quantity:] + r_binary[-bits_quantity:]
	elif channel == "ABRG":
		return a_binary[-bits_quantity:] + b_binary[-bits_quantity:] + r_binary[-bits_quantity:] + g_binary[-bits_quantity:]
	elif channel == "RGB":
		return r_binary[-bits_quantity:] + g_binary[-bits_quantity:] + b_binary[-bits_quantity:]
	elif channel == "RBG":
		return r_binary[-bits_quantity:] + b_binary[-bits_quantity:] + g_binary[-bits_quantity:]
	elif channel == "GRB":
		return g_binary[-bits_quantity:] + r_binary[-bits_quantity:] + b_binary[-bits_quantity:]
	elif channel == "GBR":
		return g_binary[-bits_quantity:] + b_binary[-bits_quantity:] + r_binary[-bits_quantity:]
	elif channel == "BGR":
		return b_binary[-bits_quantity:] + g_binary[-bits_quantity:] + r_binary[-bits_quantity:]
	elif channel == "BRG":
		return b_binary[-bits_quantity:] + r_binary[-bits_quantity:] + g_binary[-bits_quantity:]
	elif channel == "AGB":
		return a_binary[-bits_quantity:] + g_binary[-bits_quantity:] + b_binary[-bits_quantity:]
	elif channel == "ABG":
		return a_binary[-bits_quantity:] + b_binary[-bits_quantity:] + g_binary[-bits_quantity:]
	elif channel == "GAB":
		return g_binary[-bits_quantity:] + a_binary[-bits_quantity:] + b_binary[-bits_quantity:]
	elif channel == "GBA":
		return g_binary[-bits_quantity:] + b_binary[-bits_quantity:] + a_binary[-bits_quantity:]
	elif channel == "BGA":
		return b_binary[-bits_quantity:] + g_binary[-bits_quantity:] + a_binary[-bits_quantity:]
	elif channel == "BAG":
		return b_binary[-bits_quantity:] + a_binary[-bits_quantity:] + g_binary[-bits_quantity:]
	elif channel == "RAB":
		return r_binary[-bits_quantity:] + a_binary[-bits_quantity:] + b_binary[-bits_quantity:]
	elif channel == "RBA":
		return r_binary[-bits_quantity:] + b_binary[-bits_quantity:] + a_binary[-bits_quantity:]
	elif channel == "ARB":
		return a_binary[-bits_quantity:] + r_binary[-bits_quantity:] + b_binary[-bits_quantity:]
	elif channel == "ABR":
		return a_binary[-bits_quantity:] + b_binary[-bits_quantity:] + r_binary[-bits_quantity:]
	elif channel == "BAR":
		return b_binary[-bits_quantity:] + a_binary[-bits_quantity:] + r_binary[-bits_quantity:]
	elif channel == "BRA":
		return b_binary[-bits_quantity:] + r_binary[-bits_quantity:] + a_binary[-bits_quantity:]
	elif channel == "RGA":
		return r_binary[-bits_quantity:] + g_binary[-bits_quantity:] + a_binary[-bits_quantity:]
	elif channel == "RAG":
		return r_binary[-bits_quantity:] + a_binary[-bits_quantity:] + g_binary[-bits_quantity:]
	elif channel == "GRA":
		return g_binary[-bits_quantity:] + r_binary[-bits_quantity:] + a_binary[-bits_quantity:]
	elif channel == "GAR":
		return g_binary[-bits_quantity:] + a_binary[-bits_quantity:] + r_binary[-bits_quantity:]
	elif channel == "AGR":
		return a_binary[-bits_quantity:] + g_binary[-bits_quantity:] + r_binary[-bits_quantity:]
	elif channel == "ARG":
		return a_binary[-bits_quantity:] + r_binary[-bits_quantity:] + g_binary[-bits_quantity:]
	elif channel == "RG":
		return r_binary[-bits_quantity:] + g_binary[-bits_quantity:]
	elif channel == "RA":
		return r_binary[-bits_quantity:] + a_binary[-bits_quantity:]
	elif channel == "RB":
		return r_binary[-bits_quantity:] + b_binary[-bits_quantity:]
	elif channel == "GA":
		return g_binary[-bits_quantity:] + a_binary[-bits_quantity:]
	elif channel == "GB":
		return g_binary[-bits_quantity:] + b_binary[-bits_quantity:]
	elif channel == "GR":
		return g_binary[-bits_quantity:] + r_binary[-bits_quantity:]
	elif channel == "BA":
		return b_binary[-bits_quantity:] + a_binary[-bits_quantity:]
	elif channel == "BG":
		return b_binary[-bits_quantity:] + g_binary[-bits_quantity:]
	elif channel == "BR":
		return b_binary[-bits_quantity:] + r_binary[-bits_quantity:]
	elif channel == "AR":
		return a_binary[-bits_quantity:] + r_binary[-bits_quantity:]
	elif channel == "AG":
		return a_binary[-bits_quantity:] + g_binary[-bits_quantity:]
	elif channel == "AB":
		return a_binary[-bits_quantity:] + b_binary[-bits_quantity:]
	elif channel == "R":
		return r_binary[-bits_quantity:]
	elif channel == "B":
		return b_binary[-bits_quantity:]
	elif channel == "G":
		return g_binary[-bits_quantity:]
	elif channel == "A":
		return a_binary[-bits_quantity:]


def binary_to_ascii(binary_string):
	"""Basic function that takes a binary string in parameters. e.g: '00111010101010' and transform it to an ascii
	string.
	"""
	binary_bytes = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]

	buff = ''
	for character in binary_bytes:
		buff += chr(int(character, 2))

	return buff