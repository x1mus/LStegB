#!/usr/bin/python3

try:
	from PIL import Image
	from progress.bar import IncrementalBar
except ModuleNotFoundError:
	print("\033[1;31m" + "Please install the requirements")
	exit()

from common import rgba_to_binary, la_to_binary, binary_to_ascii


class Basic:
	def __init__(self, im, bits_quantity, channels, steps):
		self.im = im
		self.width, self.height = im.size
		self.bits_quantity = bits_quantity
		self.channels = channels
		self.steps = steps

	def main(self, bit, channel, height_step, width_step, reversed_height, reversed_width):
		""" We browse the image in every directions (bottom -> top / right -> left / ...) and for each directions, we write
		the results ascii strings in the basic.txt file.
		"""
		range_height_pixel = range(0, self.height, height_step)
		range_width_pixel = range(0, self.width, width_step)

		if reversed_width:
			range_width_pixel = reversed(range_width_pixel)
		if reversed_height:
			range_height_pixel = reversed(range_height_pixel)

		f = open("basic.txt", "a", encoding="utf-8")

		# Foreach height, we browse the whole width
		pixels = self.im.load()
		secret = ''
		for height_pixel in range_height_pixel:
			for width_pixel in range_width_pixel:
				if self.im.mode == "L":
					l = pixels[width_pixel, height_pixel]
					secret += la_to_binary(bit, channel, l)
				elif self.im.mode == "LA":
					l, a = pixels[width_pixel, height_pixel]
					secret += la_to_binary(bit, channel, l, a)
				elif self.im.mode == "RGB":
					r, g, b = pixels[width_pixel, height_pixel]
					secret += rgba_to_binary(bit, channel, r, g, b)
				elif self.im.mode == "RGBA":
					r, g, b, a = pixels[width_pixel, height_pixel]
					secret += rgba_to_binary(bit, channel, r, g, b, a)

		f.write(binary_to_ascii(secret))

		# Foreach width, we browse the whole height
		pixels = self.im.load()
		secret = ''
		for width_pixel in range_width_pixel:
			for height_pixel in range_height_pixel:
				if self.im.mode == "L":
					l = pixels[width_pixel, height_pixel]
					secret += la_to_binary(bit, channel, l)
				elif self.im.mode == "LA":
					l, a = pixels[width_pixel, height_pixel]
					secret += la_to_binary(bit, channel, l, a)
				elif self.im.mode == "RGB":
					r, g, b = pixels[width_pixel, height_pixel]
					secret += rgba_to_binary(bit, channel, r, g, b)
				elif self.im.mode == "RGBA":
					r, g, b, a = pixels[width_pixel, height_pixel]
					secret += rgba_to_binary(bit, channel, r, g, b, a)

		f.write(binary_to_ascii(secret))

		f.close()

	def bruteforce(self):
		""" 1. Run trough all possibilities of bits
			2. Run through every combinations possible of channel
			3. Setting up the step amount to maximum 10 (vertically and horizontally)
			4. Calling the basic process to browse the image in different directions
		"""
		maximum = len(self.bits_quantity) * len(self.channels) * len(self.steps)**2 * 5
		bar = IncrementalBar('Processing', max=maximum, suffix='%(percent)d%%')
		for bit in self.bits_quantity:
			for channel in self.channels:
				for height_step in self.steps:
					for width_step in self.steps:
						bar.next()
						self.main(bit, channel, height_step, width_step, False, False)
						bar.next()
						self.main(bit, channel, height_step, width_step, False, True)
						bar.next()
						self.main(bit, channel, height_step, width_step, True, False)
						bar.next()
						self.main(bit, channel, height_step, width_step, True, True)
						bar.next()
		bar.finish()