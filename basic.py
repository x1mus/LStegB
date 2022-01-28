#!/usr/bin/python3

try:
	from PIL import Image
	from progress.bar import Bar
except ModuleNotFoundError:
	print("\033[1;31m" + "Please install the requirements")
	exit()


class Basic:
	def __init__(self, im, bits_quantity, channels, steps):
		self.im = im
		self.width, self.height = im.size
		self.bits_quantity = bits_quantity
		self.channels = channels
		self.steps = steps

	def main(self, im, width, height, bit, channel, height_step, width_step, reversed_height, reversed_width):
		""" We browse the image in every directions (bottom -> top / right -> left / ...) and for each directions, we write
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
				if im.mode == "L":
				elif im.mode == "LA":
				elif im.mode == "RGB":
					r, g, b = pixels[width_pixel, height_pixel]
					secret += rgb_to_binary(bit, channel, r, g, b)
				elif.im.mode == "RGBA":
					r, g, b, a = pixels[width_pixel, height_pixel]
					secret += rgb_to_binary(bit, channel, r, g, b, a)

		f.write(binary_to_ascii(secret))

		# Foreach width, we browse the whole height
		pixels = im.load()
		secret = ''
		for width_pixel in range_width_pixel:
			for height_pixel in range_height_pixel:
				if im.mode == "L":
				elif im.mode == "LA":
				elif im.mode == "RGB":
					r, g, b = pixels[width_pixel, height_pixel]
					secret += rgb_to_binary(bit, channel, r, g, b)
				elif.im.mode == "RGBA":
					r, g, b, a = pixels[width_pixel, height_pixel]
					secret += rgb_to_binary(bit, channel, r, g, b, a)

		f.write(binary_to_ascii(secret))

		f.close()

	def bruteforce(self):
		""" 1. Run trough all possibilities of bits
			2. Run through every combinations possible of channel
			3. Setting up the step amount to maximum 10 (vertically and horizontally)
			4. Calling the basic process to browse the image in different directions
		"""

		bar = Bar('Processing', max=3645, suffix='%(percent)d%%')
		for bit in self.bits_quantity:
			for channel in self.channels:
				for height_step in self.steps:
					for width_step in self.steps:
						self.basic(self.im, self.width, self.height, bit, channel, height_step, width_step, False, False)
						self.basic(self.im, self.width, self.height, bit, channel, height_step, width_step, False, True)
						self.basic(self.im, self.width, self.height, bit, channel, height_step, width_step, True, False)
						self.basic(self.im, self.width, self.height, bit, channel, height_step, width_step, True, True)
						bar.next()
		bar.finish()