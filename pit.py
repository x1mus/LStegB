#!/usr/bin/python3

try:
	from PIL import Image
	from progress.bar import IncrementalBar
except ModuleNotFoundError:
	print("\033[1;31m" + "Please install the requirements")
	exit()

from common import parity_bit, is_prime, binary_to_ascii

class Pit:
	def __init__(self, im, steps):
		self.im = im
		self.width, self.height = im.size
		self.steps = steps
		self.channels = ["RGB", "RBG", "GRB", "GBR", "BGR", "BRG"]

	def get_secret_length(self, reversed_height, reversed_width, vertical):
		"""Since PIT is based on an indicator channel determined by the size of the secret, we need to find it.
		The secret length is always in the first row of the image (in the first 8 bytes (so 3 pixels - 1 byte))
		"""
		pixels = self.im.load()
		secret_length_binary = ''

		i = 0
		while i < 3:
			if vertical:
				if reversed_width and reversed_height:
					r, g, b = pixels[self.width - 1, self.height - i - 1]
				elif reversed_width:
					r, g, b = pixels[self.width - 1, i]
				elif reversed_height:
					r, g, b = pixels[0, self.height - i - 1]
				else:
					r, g, b = pixels[0, i]
			else:
				if reversed_width and reversed_height:
					r, g, b = pixels[self.width - i - 1, self.height - 1]
				elif reversed_width:
					r, g, b = pixels[self.width - i - 1, 0]
				elif reversed_height:
					r, g, b = pixels[i, self.height - 1]
				else:
					r, g, b = pixels[i, 0]

			r_binary = '{0:08b}'.format(r)
			g_binary = '{0:08b}'.format(g)
			b_binary = '{0:08b}'.format(b)

			secret_length_binary += r_binary + g_binary + b_binary

			i += 1

		secret_length = secret_length_binary[:-8]
		return int(secret_length, 2) // 8

	def find_pattern(self, secret_length):
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


	def extract_bits(self, indicator, channel1, channel2):
		if indicator[-2:] == "01":
			return str(channel2[-2:])
		elif indicator[-2:] == "10":
			return str(channel1[-2:])
		elif indicator[-2:] == "11":
			return str(channel1[-2:] + channel2[-2:])
		else:
			return ""

	def main(self, height_step, width_step, reversed_height, reversed_width):
		"""The first part of this function browse the image horizontally starting on :
			- top left
			- top right
			- bottom left
			- bottom right
		For each direction, we get the secret_length to discover the pattern. Finally, we extracts all necessary bits and
		then decode them to ASCII
		"""
		secret_length = self.get_secret_length(reversed_height, reversed_width, False)
		pattern = self.find_pattern(secret_length)

		f = open("pit.txt", "a", encoding="utf-8")

		if not reversed_height:
			range_height_pixel = range(1, self.height, height_step)
		else:
			range_height_pixel = reversed(range(0, self.height - 1, height_step))

		if not reversed_width:
			range_width_pixel = range(0, self.width, width_step)
		else:
			range_width_pixel = reversed(range(0, self.width, width_step))

		pixels = self.im.load()
		secret = ''
		for height_pixel in range_height_pixel:
			for width_pixel in range_width_pixel:
				r, g, b = pixels[width_pixel, height_pixel]

				r_binary = '{0:08b}'.format(r)
				g_binary = '{0:08b}'.format(g)
				b_binary = '{0:08b}'.format(b)

				if pattern == "RGB":
					secret += self.extract_bits(r_binary, g_binary, b_binary)
				elif pattern == "RBG":
					secret += self.extract_bits(r_binary, b_binary, g_binary)
				elif pattern == "BGR":
					secret += self.extract_bits(b_binary, g_binary, r_binary)
				elif pattern == "BRG":
					secret += self.extract_bits(b_binary, r_binary, g_binary)
				elif pattern == "GBR":
					secret += self.extract_bits(g_binary, b_binary, r_binary)
				elif pattern == "GRB":
					secret += self.extract_bits(g_binary, r_binary, b_binary)

		f.write(binary_to_ascii(secret))
		f.close()

		"""This second part focus on browsing the image vertically and doing the same operations than before
		"""
		secret_length = self.get_secret_length(reversed_height, reversed_width, True)
		pattern = self.find_pattern(secret_length)

		f = open("pit.txt", "a", encoding="utf-8")

		if not reversed_height:
			range_height_pixel = range(0, self.height, height_step)
		else:
			range_height_pixel = reversed(range(0, self.height, height_step))

		if not reversed_width:
			range_width_pixel = range(1, self.width, width_step)
		else:
			range_width_pixel = reversed(range(0, self.width - 1, width_step))

		pixels = self.im.load()
		secret = ''
		for width_pixel in range_width_pixel:
			for height_pixel in range_height_pixel:
				r, g, b = pixels[width_pixel, height_pixel]

				r_binary = '{0:08b}'.format(r)
				g_binary = '{0:08b}'.format(g)
				b_binary = '{0:08b}'.format(b)

				if pattern == "RGB":
					secret += self.extract_bits(r_binary, g_binary, b_binary)
				elif pattern == "RBG":
					secret += self.extract_bits(r_binary, b_binary, g_binary)
				elif pattern == "BGR":
					secret += self.extract_bits(b_binary, g_binary, r_binary)
				elif pattern == "BRG":
					secret += self.extract_bits(b_binary, r_binary, g_binary)
				elif pattern == "GBR":
					secret += self.extract_bits(g_binary, b_binary, r_binary)
				elif pattern == "GRB":
					secret += self.extract_bits(g_binary, r_binary, b_binary)

		f.write(binary_to_ascii(secret))
		f.close()

	def bruteforce(self):
		""" Only bruteforcing the steps and directions. Rest is provided by the Pixel Indicator Technique itself.
		"""
		maximum = len(self.steps)**2 * 5
		bar = IncrementalBar('Processing', max=maximum, suffix='%(percent)d%%')
		for height_step in self.steps:
			for width_step in self.steps:
				bar.next()
				self.main(height_step, width_step, False, False)
				bar.next()
				self.main(height_step, width_step, False, True)
				bar.next()
				self.main(height_step, width_step, True, False)
				bar.next()
				self.main(height_step, width_step, True, True)
				bar.next()
		bar.finish()