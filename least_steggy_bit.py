#!/usr/bin/python3

import os
import magic
import argparse
from progress.bar import Bar
from termcolor import colored
from PIL import Image, UnidentifiedImageError

class LeastSteganographicBit:
	def __init__(self):
		self.parser = argparse.ArgumentParser()
		self.parser.add_argument("--file", "-f", type=str, required=True, help="File to brute-force")
		self.parser.add_argument("--all", "-a", action="store_true", help="Using all LSB techniques")
		self.parser.add_argument("--basic", "-b", action="store_true", help="Basic LSB")
		self.parser.add_argument("--pit", "-i", action="store_true", help="Pixel indicator technique")
		self.parser.add_argument("--pvd", "-v", action="store_true", help="Pixel value differenciation")
		self.args = self.parser.parse_args()
		self.file = self.args.file
		self.all = self.args.all
		self.basic = self.args.basic
		self.pit = self.args.pit
		self.pvd = self.args.pvd

		# At least 1 action requested
		if not (self.all or self. basic or self.pit or self.pvd):
			self.parser.error("No action requested, add -a, -b, -i or -v")

		# Making sure the file exist
		try:
			self.type = magic.from_file(self.file, mime=True)
		except:
			print(colored("File not found", "red", attrs=['bold']))
			exit()

		# Checking if the file formats are JPEG or PNG
		if "jpeg" in self.type or "png" in self.type:
			self.im = Image.open(self.file)
		else:
			print(colored("File format not supported", "red", attrs=['bold']))
			exit()

		self.width, self.height = self.im.size

	def basic_bf(self, bits_quantity, channel, height_step = 1, width_step = 1, reversed_width = False, reversed_height = False):
		f = open("basic.txt", "a")
		
		pixels = self.im.load()
		height_pixel_range = range(0, self.height, height_step)
		width_pixel_range = range(0, self.width, width_step)
		
		if reversed_width :
			width_pixel_range = reversed(width_pixel_range)
		if reversed_height :
			height_pixel_range = reversed(height_pixel_range)

		# Foreach height, we're browsing all the width
		secret = ''
		for height_pixel in height_pixel_range:
			for width_pixel in width_pixel_range:
				r, g, b = pixels[width_pixel, height_pixel]

				secret += rgb_to_binary(bits_quantity, channel, r, g, b)

		f.write(binary_to_ascii(secret))

		# Foreach width, we're browsing all the height
		secret = ''
		for width_pixel in width_pixel_range:
			for height_pixel in height_pixel_range:
				r, g, b = pixels[width_pixel, height_pixel]

				secret += rgb_to_binary(bits_quantity, channel, r, g, b)

		f.write(binary_to_ascii(secret))

		f.close()


def rgb_to_binary(bits_quantity, channel, r, g, b):
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
	binary_bytes = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]

	buff = ''
	for character in binary_bytes:
		buff += chr(int(character, 2))

	return buff

def main():
	leastSteganographicBit = LeastSteganographicBit()
	print(colored("This program can take quite some time to complete.", "red", attrs=['bold']))
	print(colored("[+]", "green") + " Starting LeastSteganographicBit program...")
	os.mkdir("./LSB/")
	os.chdir("./LSB/")

	if leastSteganographicBit.all or leastSteganographicBit.basic:
		print(colored("[+]", "green") + " Starting basic process...")
		channels = ["RGB", "RBG", "GRB", "GBR", "BGR", "BRG", "RG", "RB", "GR", "GB", "BR", "BG", "R", "G", "B"]
		bar = Bar('Processing', max=3645, suffix='%(percent)d%%')
		for bits_quantity in range(1, 4):
			for channel in channels:
				for height_step in range(1, 10):
					for width_step in range(1, 10):
						leastSteganographicBit.basic_bf(bits_quantity, channel, height_step, width_step)
						leastSteganographicBit.basic_bf(bits_quantity, channel, height_step, width_step, reversed_height = True)
						leastSteganographicBit.basic_bf(bits_quantity, channel, height_step, width_step, reversed_width = True)
						leastSteganographicBit.basic_bf(bits_quantity, channel, height_step, width_step, reversed_width = True, reversed_height = True)
						bar.next()
		bar.finish()
		print(colored("[-]", "red") + " Ending basic process...")

	print(colored("[-]", "red") + " Ending LeastSteganographicBit program...")

if __name__ == "__main__":
	main()

"""PIXEL INDICATOR TECHNIQUE
		from PIL import Image
		import binascii

		def is_prime(num):
			return all(num % i for i in range(2, num))

		def parity_bit(num):
			binary = bin(num).replace("0b", "")
			count = str(binary).count('1')

			return True if count % 2 == 0 else False

		def get_secret_size(pixels):
			secret_length = ''
			i = 0
			
			while i < 3:
				r, g, b = pixels[i, 0]

				r_binary = '{0:08b}'.format(r)
				g_binary = '{0:08b}'.format(g)
				b_binary = '{0:08b}'.format(b)

				secret_length += r_binary + g_binary + b_binary

				i += 1

			secret_length = secret_length[:-8]
			return int(secret_length, 2)//8

		def find_pattern(secret_length):
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
				return channel2[-2:]
			elif indicator[-2:] == "10":
				return channel1[-2:]
			elif indicator[-2:] == "11":
				return channel1[-2:] + channel2[-2:]

		def extract_secret(pattern, pixels, width, height):
			secret = ''

			for height_pixel in range(1, height):
				for width_pixel in range(0, width):
					r, g, b = pixels[width_pixel, height_pixel]

					r_binary = '{0:08b}'.format(r)
					g_binary = '{0:08b}'.format(g)
					b_binary = '{0:08b}'.format(b)

					if pattern == "RGB":
						secret += str(extract_bits(r_binary, g_binary, b_binary))
					elif pattern == "RBG":
						secret += str(extract_bits(r_binary, b_binary, g_binary))
					elif pattern == "BGR":
						secret += str(extract_bits(b_binary, g_binary, r_binary))
					elif pattern == "BRG":
						secret += str(extract_bits(b_binary, r_binary, g_binary))
					elif pattern == "GBR":
						secret += str(extract_bits(g_binary, b_binary, r_binary))
					elif pattern == "GRB":
						secret += str(extract_bits(g_binary, r_binary, b_binary))
					else:
						print("Unrecognized pattern")

			secret = secret.replace("None", "")

			return secret

		im = Image.open("ch13.png")
		width, height = im.size
		pixels = im.load()

		secret_length = get_secret_size(pixels)
		pattern = find_pattern(secret_length)
		secret = extract_secret(pattern, pixels, width, height)

		secret = [secret[i:i+8] for i in range(0, secret_length*8, 8)]

		for character in secret:
			print(chr(int(character, 2)), end='')"""

"""Pixel Vallue Differenciation
		from PIL import Image
		import math

		def pixel_diff(i, j):
			return abs(pixels[i, j] - pixels[i+1, j])

		def get_lower_range(diff):
			if diff >= 0 and diff < 8:
				return 0
			elif diff >= 8 and diff < 16:
				return 8
			elif diff >= 16 and diff < 32:
				return 16
			elif diff >= 32 and diff < 64:
				return 32
			elif diff >= 64 and diff < 128:
				return 64
			elif diff >= 128 and diff < 256:
				return 128

		def rangeWidth(diff):
			if diff >= 0 and diff < 16:
				return 8
			if diff >= 16 and diff < 32:
				return 16
			if diff >= 32 and diff < 64:
				return 32
			if diff >= 64 and diff < 128:
				return 64
			if diff >= 128 and diff < 256:
				return 128

		def extract_secret(width_pixel, height_pixel):
			diff = pixel_diff(width_pixel, height_pixel)
			number = diff - get_lower_range(diff)
			binary = str(bin(number)[2:])

			while len(binary) < math.log(rangeWidth(diff), 2):
				binary = "0" + binary
			while len(binary) > math.log(rangeWidth(diff), 2):
				binary = binary[1:]

			return binary

		im = Image.open("ch12.png")
		width, height = im.size
		pixels = im.load()

		secret = ''

		for height_pixel in range(0, height, 2):
			for width_pixel in range(0, width, 2):
				secret += extract_secret(width_pixel, height_pixel)
			for width_pixel in reversed(range(0, width, 2)):
				secret += extract_secret(width_pixel, height_pixel+1)

		secret = [secret[i:i+8] for i in range(0, len(secret), 8)]
		for character in secret:
			print(chr(int(character, 2)), end='')
		"""