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
	""" Getting all arguments passed to the program
	"""
	parser.add_argument("--file", "-f", type=str, required=True, help="Image to brute-force")
	parser.add_argument("--all", "-a", action="store_true", help="All LSB techniques")
	parser.add_argument("--basic", "-b", action="store_true", help="Basic LSB")
	parser.add_argument("--pit", "-i", action="store_true", help="Pixel indicator technique")
	parser.add_argument("--pvd", "-v", action="store_true", help="Pixel value differencing")
	args = parser.parse_args()
	return args


def check_arguments(parser, args):
	"""Making sure the file passed is a valid image & exist.
	Then we need to be sure that the user uses valid arguments
	"""
	try:
		if imghdr.what(args.file) != "jpeg" and imghdr.what(args.file) != "png":
			parser.error("The file is not a valid image")
	except FileNotFoundError:
		parser.error("File not found")

	if not args.all and not args.basic and not args.pit and not args.pvd:
		parser.error("Please specify at least one technique (-b / -i / -v)")
	elif args.all and (args.basic or args.pit or args.pvd):
		parser.error("If -a is specified, you can't specify -b, -i or -v")


def rgb_to_binary(bits_quantity, channel, r, g, b):
	"""Takes the quantity of bits, to keep (from 1 to 3) in each channel in parameter.
	For example: We can take the 2 last bits of the R & B channels only
	"""
	r_binary = '{0:08b}'.format(r)
	g_binary = '{0:08b}'.format(g)
	b_binary = '{0:08b}'.format(b)

	if channel == "RGB":
		return r_binary[-bits_quantity:] + g_binary[-bits_quantity:] + b_binary[-bits_quantity:]
	elif channel == "RBG":
		return r_binary[-bits_quantity:] + b_binary[-bits_quantity:] + g_binary[-bits_quantity:]
	elif channel == "GBR":
		return g_binary[-bits_quantity:] + b_binary[-bits_quantity:] + r_binary[-bits_quantity:]
	elif channel == "GRB":
		return g_binary[-bits_quantity:] + r_binary[-bits_quantity:] + b_binary[-bits_quantity:]
	elif channel == "BGR":
		return b_binary[-bits_quantity:] + g_binary[-bits_quantity:] + r_binary[-bits_quantity:]
	elif channel == "BRG":
		return b_binary[-bits_quantity:] + r_binary[-bits_quantity:] + g_binary[-bits_quantity:]
	elif channel == "RG":
		return r_binary[-bits_quantity:] + g_binary[-bits_quantity:]
	elif channel == "RB":
		return r_binary[-bits_quantity:] + b_binary[-bits_quantity:]
	elif channel == "GB":
		return g_binary[-bits_quantity:] + b_binary[-bits_quantity:]
	elif channel == "GR":
		return g_binary[-bits_quantity:] + r_binary[-bits_quantity:]
	elif channel == "BR":
		return b_binary[-bits_quantity:] + r_binary[-bits_quantity:]
	elif channel == "BG":
		return b_binary[-bits_quantity:] + g_binary[-bits_quantity:]
	elif channel == "R":
		return r_binary[-bits_quantity:]
	elif channel == "G":
		return g_binary[-bits_quantity:]
	elif channel == "B":
		return b_binary[-bits_quantity:]


def binary_to_ascii(binary_string):
	"""Basic function that takes a binary string in parameters. e.g: '00111010101010' and transform it to an ascii
	string.
	"""
	binary_bytes = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]

	buff = ''
	for character in binary_bytes:
		buff += chr(int(character, 2))

	return buff


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
			r, g, b = pixels[width_pixel, height_pixel]

			secret += rgb_to_binary(bit, channel, r, g, b)
	f.write(binary_to_ascii(secret))

	# Foreach width, we browse the whole height
	pixels = im.load()
	secret = ''
	for width_pixel in range_width_pixel:
		for height_pixel in range_height_pixel:
			r, g, b = pixels[width_pixel, height_pixel]

			secret += rgb_to_binary(bit, channel, r, g, b)
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


def main():
	"""First of all, we do all the requirements before starting the program. In includes:
		- Checking the file
		- Verifying all the arguments that the users passed to the program
	"""
	parser = argparse.ArgumentParser()
	args = get_arguments(parser)
	check_arguments(parser, args)

	"""Since all the verifications succeeded if we reach this point, we're starting the process according to the
	arguments and defining the variable that will not change throughout the whole program
	"""
	channels = ["RGB", "RBG", "GRB", "GBR", "BGR", "BRG", "RG", "RB", "GR", "GB", "BR", "BG", "R", "G", "B"]
	bits_quantity = range(1, 4)
	steps = range(1, 10)
	im = Image.open(args.file)
	width, height = im.size

	print(colored("This program can take quite some time to complete.", "red", attrs=['bold']))
	print(colored("[+]", "green") + " Starting LStegB program...")

	if args.all:
		print(colored("[+]", "green") + " Starting basic process...")
		basic_bf(im, width, height, bits_quantity, channels, steps)
		print(colored("[-]", "red") + " Ending basic process...")
		print(colored("[+]", "green") + " Starting pit process...")
		# pit(im, width, height)
		print(colored("[-]", "red") + " Ending pit process...")
		print(colored("[+]", "green") + " Starting pvd process...")
		# pvd(im, width, height)
		print(colored("[-]", "red") + " Ending pvd process...")
	else:
		if args.basic:
			print(colored("[+]", "green") + " Starting basic process...")
			basic_bf(im, width, height, bits_quantity, channels, steps)
			print(colored("[-]", "red") + " Ending basic process...")
		if args.pit:
			print(colored("[+]", "green") + " Starting pit process...")
			# pit(im, width, height)
			print(colored("[-]", "red") + " Ending pit process...")
		if args.pvd:
			print(colored("[+]", "green") + " Starting pvd process...")
			# pvd(im, width, height)
			print(colored("[-]", "red") + " Ending pvd process...")

	print(colored("[-]", "red") + " Ending LStegB program...")


if __name__ == "__main__":
	main()
