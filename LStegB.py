#!/usr/bin/python3

try:
	import os, imghdr, argparse
	from termcolor import colored
	from PIL import Image
except ModuleNotFoundError:
	print("\033[1;31m" + "Please install the requirements")
	exit()

from basic import Basic
from pit import Pit


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
			- "P" --> Indexed-color (palette)
			- Other are not supported right now
		"""
		mode = self.im.mode
		if mode in ["L", "LA", "RGB", "RGBA", "P"]:
			print(f"{colored('[+]', 'green')} PNG type '{mode}' detected")
			if mode == "L":
				self.channels = self.l_combination
			elif mode == "LA":
				self.channels = self.la_combination
			elif mode == "RGB":
				self.channels = self.rgb_combination
			elif mode == "RGBA":
				self.channels = self.rgba_combination
			elif mode == "P":
				plte_mode = self.im.palette.getdata()[0]
				if plte_mode == "RGB":
					self.channels = self.rgb_combination
				else:
					print(f"{colored('[-]', 'red')} PNG type '{mode}' with '{plte_mode}' is not supported")
					exit()
		else:
			print(f"{colored('[-]', 'red')} PNG type '{mode}' is not supported")
			exit()

	def run(self):
		self.im = Image.open(self.args.file)

		if self.file_type == "png":
			self.find_png_type()

		print(f"{colored('[+]', 'green')} Starting LStegB program...")

		if self.args.all:
			print(f"{colored('[+]', 'green')} Starting basic process...")
			basic = Basic(self.im, self.bits_quantity, self.channels, self.steps)
			basic.bruteforce()
			print(f"{colored('[-]', 'red')} Ending basic process...")
			print(f"{colored('[+]', 'green')} Starting pit process...")
			if self.im.mode != "RGB":
				print(colored("PIT only supports RGB files", "red"))
			else:
				pit = Pit(self.im, self.steps)
				pit.bruteforce()
			print(f"{colored('[-]', 'red')} Ending pit process...")
		else:
			if self.args.basic:
				print(f"{colored('[+]', 'green')} Starting basic process...")
				basic = Basic(self.im, self.bits_quantity, self.channels, self.steps)
				basic.bruteforce()
				print(f"{colored('[-]', 'red')} Ending basic process...")
			if self.args.pit:
				print(f"{colored('[+]', 'green')} Starting pit process...")
				if self.im.mode != "RGB":
					print(colored("PIT only supports RGB files", "red"))
				else:
					pit = Pit(self.im, self.steps)
					pit.bruteforce()
				print(f"{colored('[-]', 'red')} Ending pit process...")

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