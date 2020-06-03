from random import *


class Grid:
	def __init__(self, height=10, width=10, wall=1):
		self.height = height
		self.width = width
		self.wall = wall
		self.map = []
		for y in range(self.height):
			row = []
			for x in range(self.width):
				row.append(choices([0, 1], weights=[10, self.wall])[0])
			self.map.append(row)


