#!/usr/bin/python3

import binascii
from PIL import Image

# Loading the image
im = Image.open("samples/png/indexed_color_8-bit-depth.png")
pixels = im.load()

index = pixels[0, 0] # Since the pixel value is only an index to the palette

# Getting the palette
datas = im.palette.getdata() # Experimental method in the doc
mode = datas[0] # example = 'RGB'
plte = binascii.hexlify(datas[1]).decode("utf-8") # This return a long HEX string

# Splitting the HEX string into group of 6 (RGB) (if RGBA then 8)
result = []
for i in range(0, len(plte), 6):
	entry = plte[i:i+6]
	# Converting each group into a triple
	triple = (int(entry[0:2],16), int(entry[2:4],16), int(entry[4:6],16))
	result.append(triple)
plte = result

print(f"Palette : {plte}")
print(f"The color of the first pixel is {plte[index]}")

class Plte:
	def __init__(self):
		pass

	def main(self):
		pass

	def bruteforce(self):
		pass