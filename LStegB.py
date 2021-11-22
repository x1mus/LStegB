#!/usr/bin/python3

try:
	import os
	import imghdr
	import argparse
	from progress.bar import Bar
	from termcolor import colored
	from PIL import Image, UnidentifiedImageError
except ModuleNotFoundError:
	print("\033[1;31m" + "Please install the requirements")
	exit()


def get_arguments(parser):
	"""Getting all arguments passed to the program
	"""
	parser.add_argument("--file", "-f", type=str, required=True, help="Image to brute-force")
	parser.add_argument("--all", "-a", action="store_true", help="All LSB techniques")
	parser.add_argument("--basic", "-b", action="store_true", help="Basic LSB")
	parser.add_argument("--pit", "-i", action="store_true", help="Pixel indicator technique")
	args = parser.parse_args()
	return args


def check_arguments(parser, args):
	"""Making sure the file passed is a valid image & exist.
	Then we need to be sure that the user uses valid arguments
	"""
	try:
		if imghdr.what(args.file) != "jpeg" and imghdr.what(args.file) != "png" and imghdr.what(args.file) != "bmp":
			parser.error("The file is not a valid image")
	except FileNotFoundError:
		parser.error("File not found")

	if not args.all and not args.basic and not args.pit:
		parser.error("Please specify at least one technique (-b / -i)")
	elif args.all and (args.basic or args.pit):
		parser.error("If -a is specified, you can't specify -b or -i")


def rgb_to_binary(bits_quantity, channel, r, g, b, a=None):
	"""Takes the quantity of bits, to keep (from 1 to 3) in each channel in parameter.
	For example: We can take the 2 last bits of the R & B channels only
	"""
	r_binary = '{0:08b}'.format(r)
	g_binary = '{0:08b}'.format(g)
	b_binary = '{0:08b}'.format(b)

	a_binary = None
	if a >= 0:
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


def is_prime(num):
	"""Check if the number in paramter is a prime number, return True if it's the case, return False otherwise
	"""
	return all(num % i for i in range(2, num))


def parity_bit(num):
	binary = bin(num).replace("0b", "")
	count = str(binary).count('1')

	return True if count % 2 == 0 else False


def basic(im, width, height, bit, channel, height_step, width_step, reversed_height, reversed_width):
	"""We browse the image in every directions (bottom -> top / right -> left / ...) and for each directions, we write
	the results ascii strings in the basic.txt file.
	"""
	range_height_pixel = range(0, height, height_step)
	range_width_pixel = range(0, width, width_step)

	if reversed_width:
		range_width_pixel = reversed(range_width_pixel)
	if reversed_height:
		range_height_pixel = reversed(range_height_pixel)

	f = open("basic.txt", "a", encoding="utf-8")

	# Foreach height, we browse the whole width
	pixels = im.load()
	secret = ''
	for height_pixel in range_height_pixel:
		for width_pixel in range_width_pixel:
			try:
				r, g, b = pixels[width_pixel, height_pixel]
				secret += rgb_to_binary(bit, channel, r, g, b)
			except ValueError:
				r, g, b, a = pixels[width_pixel, height_pixel]
				secret += rgb_to_binary(bit, channel, r, g, b, a)

	f.write(binary_to_ascii(secret))

	# Foreach width, we browse the whole height
	pixels = im.load()
	secret = ''
	for width_pixel in range_width_pixel:
		for height_pixel in range_height_pixel:
			try:
				r, g, b = pixels[width_pixel, height_pixel]
				secret += rgb_to_binary(bit, channel, r, g, b)
			except ValueError:
				r, g, b, a = pixels[width_pixel, height_pixel]
				secret += rgb_to_binary(bit, channel, r, g, b, a)

	f.write(binary_to_ascii(secret))

	f.close()


def basic_bf(im, width, height, bits_quantity, channels, steps):
	"""In this order :
		First, we're going trough all 3 possibilities of bits (1 to 3)
		Second, we're going through every combinations possible of channels (RGB / RBG / GRB / ...)
		Third & fourth, setting up step amount to maximum 10 (vertically and horizontally)
		Finally, we call the basic process to browse the image in different directions
	"""
	bar = Bar('Processing', max=3645, suffix='%(percent)d%%')
	for bit in bits_quantity:
		for channel in channels:
			for height_step in steps:
				for width_step in steps:
					basic(im, width, height, bit, channel, height_step, width_step, False, False)
					basic(im, width, height, bit, channel, height_step, width_step, False, True)
					basic(im, width, height, bit, channel, height_step, width_step, True, False)
					basic(im, width, height, bit, channel, height_step, width_step, True, True)
					bar.next()
	bar.finish()


def get_secret_length(im, width, height, reversed_height, reversed_width, vertical):
	"""Since PIT is based on an indicator channel determined by the size of the secret, we need to find it.
	The secret length is always in the first row of the image (in the first 8 bytes (so 3 pixels - 1 byte))
	"""
	pixels = im.load()
	secret_length_binary = ''

	i = 0
	while i < 3:
		if vertical:
			if reversed_width and reversed_height:
				r, g, b = pixels[width - 1, height - i - 1]
			elif reversed_width:
				r, g, b = pixels[width - 1, i]
			elif reversed_height:
				r, g, b = pixels[0, height - i - 1]
			else:
				r, g, b = pixels[0, i]
		else:
			if reversed_width and reversed_height:
				r, g, b = pixels[width - i - 1, height - 1]
			elif reversed_width:
				r, g, b = pixels[width - i - 1, 0]
			elif reversed_height:
				r, g, b = pixels[i, height - 1]
			else:
				r, g, b = pixels[i, 0]

		r_binary = '{0:08b}'.format(r)
		g_binary = '{0:08b}'.format(g)
		b_binary = '{0:08b}'.format(b)

		secret_length_binary += r_binary + g_binary + b_binary

		i += 1

	secret_length = secret_length_binary[:-8]
	return int(secret_length, 2) // 8


def find_pattern(secret_length):
	"""To find the pattern (so to find the indicator, the first channel & the second channel) we need to follow some
	rules based on the length of the secret :
		╔════════════╦══════╦═══════╦═══════╗
		║ Parity bit ║ Even ║ Prime ║ Other ║
		╠════════════╬══════╬═══════╬═══════╣
		║ Even       ║ RBG  ║ BGR   ║ GBR   ║
		╠════════════╬══════╬═══════╬═══════╣
		║ Odd        ║ RGB  ║ BRG   ║ GRB   ║
		╚════════════╩══════╩═══════╩═══════╝
		For example, if the length of the message is 17 :
			- 17 isnt even, but is a prime number --> Indicator == B
			- 17 in binary is 10001 so the parity is even --> first channel is G & second channel is R
	"""
	if secret_length % 2 == 0:
		pattern = "R"
		if parity_bit(secret_length):
			pattern += "BG"
		else:
			pattern += "GB"
	elif is_prime(secret_length):
		pattern = "B"
		if parity_bit(secret_length):
			pattern += "GR"
		else:
			pattern += "RG"
	else:
		pattern = "G"
		if parity_bit(secret_length):
			pattern += "BR"
		else:
			pattern += "RB"

	return pattern


def extract_bits(indicator, channel1, channel2):
	if indicator[-2:] == "01":
		return str(channel2[-2:])
	elif indicator[-2:] == "10":
		return str(channel1[-2:])
	elif indicator[-2:] == "11":
		return str(channel1[-2:] + channel2[-2:])
	else:
		return ""


def pit(im, width, height, height_step, width_step, reversed_height, reversed_width):
	"""The first part of this function browse the image horizontally starting on :
		- top left
		- top right
		- bottom left
		- bottom right
	For each direction, we get the secret_length to discover the pattern. Finally, we extracts all necessary bits and
	then decode them to ASCII
	"""
	secret_length = get_secret_length(im, width, height, reversed_height, reversed_width, False)
	pattern = find_pattern(secret_length)

	f = open("pit.txt", "a", encoding="utf-8")

	if not reversed_height:
		range_height_pixel = range(1, height, height_step)
	else:
		range_height_pixel = reversed(range(0, height - 1, height_step))

	if not reversed_width:
		range_width_pixel = range(0, width, width_step)
	else:
		range_width_pixel = reversed(range(0, width, width_step))

	pixels = im.load()
	secret = ''
	for height_pixel in range_height_pixel:
		for width_pixel in range_width_pixel:
			r, g, b = pixels[width_pixel, height_pixel]

			r_binary = '{0:08b}'.format(r)
			g_binary = '{0:08b}'.format(g)
			b_binary = '{0:08b}'.format(b)

			if pattern == "RGB":
				secret += extract_bits(r_binary, g_binary, b_binary)
			elif pattern == "RBG":
				secret += extract_bits(r_binary, b_binary, g_binary)
			elif pattern == "BGR":
				secret += extract_bits(b_binary, g_binary, r_binary)
			elif pattern == "BRG":
				secret += extract_bits(b_binary, r_binary, g_binary)
			elif pattern == "GBR":
				secret += extract_bits(g_binary, b_binary, r_binary)
			elif pattern == "GRB":
				secret += extract_bits(g_binary, r_binary, b_binary)

	f.write(binary_to_ascii(secret))
	f.close()

	"""This second part focus on browsing the image vertically and doing the same operations than before
	"""
	secret_length = get_secret_length(im, width, height, reversed_height, reversed_width, True)
	pattern = find_pattern(secret_length)

	f = open("pit.txt", "a", encoding="utf-8")

	if not reversed_height:
		range_height_pixel = range(0, height, height_step)
	else:
		range_height_pixel = reversed(range(0, height, height_step))

	if not reversed_width:
		range_width_pixel = range(1, width, width_step)
	else:
		range_width_pixel = reversed(range(0, width - 1, width_step))

	pixels = im.load()
	secret = ''
	for width_pixel in range_width_pixel:
		for height_pixel in range_height_pixel:
			r, g, b = pixels[width_pixel, height_pixel]

			r_binary = '{0:08b}'.format(r)
			g_binary = '{0:08b}'.format(g)
			b_binary = '{0:08b}'.format(b)

			if pattern == "RGB":
				secret += extract_bits(r_binary, g_binary, b_binary)
			elif pattern == "RBG":
				secret += extract_bits(r_binary, b_binary, g_binary)
			elif pattern == "BGR":
				secret += extract_bits(b_binary, g_binary, r_binary)
			elif pattern == "BRG":
				secret += extract_bits(b_binary, r_binary, g_binary)
			elif pattern == "GBR":
				secret += extract_bits(g_binary, b_binary, r_binary)
			elif pattern == "GRB":
				secret += extract_bits(g_binary, r_binary, b_binary)

	f.write(binary_to_ascii(secret))
	f.close()


def pit_bf(im, width, height, steps):
	"""Here we're not bruteforcing all the possibilities in the bits quantity or the channels since it is provided
	by the technique. The only thing we can brute force would be the steps to browse the image and the directions we're
	browsing it aswell
	"""
	bar = Bar('Processing', max=81, suffix='%(percent)d%%')
	for height_step in steps:
		for width_step in steps:
			pit(im, width, height, height_step, width_step, False, False)
			pit(im, width, height, height_step, width_step, False, True)
			pit(im, width, height, height_step, width_step, True, False)
			pit(im, width, height, height_step, width_step, True, True)
			bar.next()
	bar.finish()


def main():
	"""First of all, we do all the requirements before starting the program. It includes:
		- Checking the file
		- Verifying all the arguments that the user passes to the program
	"""
	parser = argparse.ArgumentParser()
	args = get_arguments(parser)
	check_arguments(parser, args)

	"""Since all the verifications succeeded if we reach this point, we're starting the process according to the
	arguments and defining the variable that will not change throughout the whole program
	"""
	print("""
██╗     ███████╗████████╗███████╗ ██████╗ ██████╗
██║     ██╔════╝╚══██╔══╝██╔════╝██╔════╝ ██╔══██╗
██║     ███████╗   ██║   █████╗  ██║  ███╗██████╔╝
██║     ╚════██║   ██║   ██╔══╝  ██║   ██║██╔══██╗
███████╗███████║   ██║   ███████╗╚██████╔╝██████╔╝
╚══════╝╚══════╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═════╝ 
""")
	im = Image.open(args.file)
	width, height = im.size

	if im.mode == "RGBA":
		channels = [
			"RGBA", "RGAB", "RAGB", "RABG", "RBGA", "RBAG", "BGRA", "BGAR", "BAGR", "BARG", "BRGA", "BRAG", "GRBA",
			"GRAB", "GARB", "GABR", "GBRA", "GBAR", "AGBR", "AGRB", "ARGB", "ARBG", "ABGR", "ABRG", "RGB", "RBG", "GRB",
			"GBR", "BGR", "BRG", "AGB", "ABG", "GAB", "GBA", "BGA", "BAG", "RAB", "RBA", "ARB", "ABR", "BAR", "BRA",
			"RGA", "RAG", "GRA", "GAR", "AGR", "ARG", "RG", "RA", "RB", "GA", "GB", "GR", "BA", "BG", "BR", "AR", "AG",
			"AB", "R", "B", "G", "A"
		]
	else:
		channels = ["RGB", "RBG", "GRB", "GBR", "BGR", "BRG", "RG", "RB", "GR", "GB", "BR", "BG", "R", "G", "B"]

	bits_quantity = range(1, 4)
	steps = range(1, 10)

	print(colored("This program can take quite some time to complete.", "red", attrs=['bold']))
	print(colored("[+]", "green") + " Starting LStegB program...")

	if args.all:
		print(colored("[+]", "green") + " Starting basic process...")
		basic_bf(im, width, height, bits_quantity, channels, steps)
		print(colored("[-]", "red") + " Ending basic process...")
		print(colored("[+]", "green") + " Starting pit process...")
		if im.mode == "RGBA":
			print(colored("PIT does not support RGBA files", "red"))
		else:
			pit_bf(im, width, height, steps)
		print(colored("[-]", "red") + " Ending pit process...")
	else:
		if args.basic:
			print(colored("[+]", "green") + " Starting basic process...")
			basic_bf(im, width, height, bits_quantity, channels, steps)
			print(colored("[-]", "red") + " Ending basic process...")
		if args.pit:
			print(colored("[+]", "green") + " Starting pit process...")
			if im.mode == "RGBA":
				print(colored("PIT does not support RGBA files", "red"))
			else:
				pit_bf(im, width, height, steps)
			print(colored("[-]", "red") + " Ending pit process...")

	print(colored("[-]", "red") + " Ending LStegB program...")


if __name__ == "__main__":
	main()
