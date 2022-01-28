#!/usr/bin/python3

try:
	import os
	import imghdr
	import argparse
	from termcolor import colored
	from PIL import Image, UnidentifiedImageError
except ModuleNotFoundError:
	print("\033[1;31m" + "Please install the requirements")
	exit()

from basic import Basic
# from pit import Pit


def is_prime(num):
	"""Check if the number in paramter is a prime number, return True if it's the case, return False otherwise
	"""
	return all(num % i for i in range(2, num))


def parity_bit(num):
	binary = bin(num).replace("0b", "")
	count = str(binary).count('1')

	return True if count % 2 == 0 else False


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


class LStegB:
	def __init__(self):
		""" Getting the arguments
		"""
		self.parser = argparse.ArgumentParser()
		self.parser.add_argument("--file", "-f", type=str, required=True, help="Image to brute-force")
		self.parser.add_argument("--all", "-a", action="store_true", help="All LSB techniques")
		self.parser.add_argument("--basic", "-b", action="store_true", help="Basic LSB")
		self.parser.add_argument("--pit", "-i", action="store_true", help="Pixel indicator technique")
		self.args = self.parser.parse_args()
		self.rgba_combination = [
			"RGBA", "RGAB", "RAGB", "RABG", "RBGA", "RBAG", "BGRA", "BGAR", "BAGR", "BARG", "BRGA", "BRAG", "GRBA",
			"GRAB", "GARB", "GABR", "GBRA", "GBAR", "AGBR", "AGRB", "ARGB", "ARBG", "ABGR", "ABRG", "RGB", "RBG", "GRB",
			"GBR", "BGR", "BRG", "AGB", "ABG", "GAB", "GBA", "BGA", "BAG", "RAB", "RBA", "ARB", "ABR", "BAR", "BRA",
			"RGA", "RAG", "GRA", "GAR", "AGR", "ARG", "RG", "RA", "RB", "GA", "GB", "GR", "BA", "BG", "BR", "AR", "AG",
			"AB", "R", "B", "G", "A"
		]
		self.rgb_combination = ["RGB", "RBG", "GRB", "GBR", "BGR", "BRG", "RG", "RB", "GR", "GB", "BR", "BG", "R", "G", "B"]
		self.la_combination = ["LA", "AL", "L", "A"]
		self.l_combination = ["L"]
		self.bits_quantity = range(1, 2)
		self.steps = range(1, 2)

	def check_arguments(self):
		""" Checking if the arguments are valid
		"""
		self.file_type = imghdr.what(self.args.file)
		try:
			if self.file_type != "png":
				self.parser.error("The file type specified is not supported")
		except FileNotFoundError:
			self.parser.error("File not found")

		if not self.args.all and not self.args.basic and not self.args.pit:
			self.parser.error("Please specify at least one technique (-b / -i)")
		elif self.args.all and (self.args.basic or self.args.pit):
			self.parser.error("If -a is specified, you can't specify -b or -i")

	def find_png_type(self):
		""" Getting the current PNG mode :
			- "L" --> Grayscale
			- "LA" --> Grayscale with alpha
			- "RGB" --> Truecolor
			- "RGBA" --> Truecolor with alpha
			- Other (like indexed-color are not supported right now)
		"""
		mode = self.im.mode
		if mode in ["L", "LA", "RGB", "RGBA"]:
			print(f"{colored('[+]', 'green')} PNG type '{mode}' detected")
			if mode == "L":
				self.channels = self.l_combination
			elif mode == "LA":
				self.channels = self.la_combination
			elif mode == "RGB":
				self.channels = self.rgb_combination
			elif mode == "RGBA":
				self.channels = self.rgba_combination
		else:
			print(f"{colored('[-]', 'red')} PNG type '{mode}' is not supported")
			exit()

	def run(self):
		print("""
██╗     ███████╗████████╗███████╗ ██████╗ ██████╗
██║     ██╔════╝╚══██╔══╝██╔════╝██╔════╝ ██╔══██╗
██║     ███████╗   ██║   █████╗  ██║  ███╗██████╔╝
██║     ╚════██║   ██║   ██╔══╝  ██║   ██║██╔══██╗
███████╗███████║   ██║   ███████╗╚██████╔╝██████╔╝
╚══════╝╚══════╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═════╝ 
""")
		
		self.im = Image.open(self.args.file)

		if self.file_type == "png":
			self.find_png_type()

		print(colored("This program can take quite some time to complete.", "red", attrs=['bold']))
		print(f"{colored('[+]', 'green')} Starting LStegB program...")

		if self.args.all:
			print(f"{colored('[+]', 'green')} Starting basic process...")
			basic = Basic(self.im, self.bits_quantity, self.channels, self.steps)
			basic.bruteforce()
			print(f"{colored('[-]', 'red')} Ending basic process...")
			"""
			print(f"{colored('[+]', 'green')} Starting pit process...")
			if im.mode == "RGBA":
				print(colored("PIT does not support RGBA files", "red"))
			else:
				pit_bf(im, width, height, steps)
			print(f"{colored('[-]', 'red')} Ending pit process...")"""
		else:
			if self.args.basic:
				print(f"{colored('[+]', 'green')} Starting basic process...")
				basic = Basic(self.im, self.bits_quantity, self.channels, self.steps)
				basic.bruteforce()
				print(f"{colored('[-]', 'red')} Ending basic process...")
			"""if self.args.pit:
				print(f"{colored('[+]', 'green')} Starting pit process...")
				if im.mode == "RGBA":
					print(colored("PIT does not support RGBA files", "red"))
				else:
					pit_bf(im, width, height, steps)
				print(f"{colored('[-]', 'red')} Ending pit process...")"""

		print(f"{colored('[-]', 'red')} Ending LStegB program...")


def main():
	# Creating the parser
	lstegb = LStegB()

	# Checking the given arguments
	lstegb.check_arguments()

	# Launching the main process if the checks are successful
	lstegb.run()


if __name__ == "__main__":
	main()