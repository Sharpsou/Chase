from tkinter import *
from random import *
import numpy as np

class Display:
	def __init__(self, experience,ratio_grid):
		self.experience = experience
		self.ratio_grid = ratio_grid
		self.init_grid()

	def init_grid(self):
		self.window_width_grid = 1280 / self.ratio_grid
		self.window_height_grid = 920 / self.ratio_grid
		self.window_marge_grid = 420 / self.ratio_grid

		self.window_grid = Tk()
		self.window_grid.title('Experience Grid')
		geometry = str(int(self.window_width_grid + self.window_marge_grid)) + 'x' + str(int(self.window_height_grid + self.window_marge_grid/2))
		self.window_grid.geometry(geometry)
		self.canvas_grid = Canvas(self.window_grid, width=self.window_width_grid, height=self.window_height_grid, bg='grey')
		# self.canvas.pack()

		# draw grid
		# distance between rows and columns
		self.vertical_dist_grid = self.window_height_grid / self.experience.grid.height
		self.horizontal_dist_grid = self.window_width_grid / self.experience.grid.width
		# rows
		for y in range(self.height):
			self.canvas_grid.create_line(0, (y + 1) * self.vertical_dist_grid, self.window_width, (y + 1) * self.vertical_dist_grid)
			self.canvas_grid.pack()
		# columns
		for x in range(self.width):
			self.canvas_grid.create_line((x + 1) * self.horizontal_dist_grid, 0, (x + 1) * self.horizontal_dist_grid, self.window_height)
			self.canvas_grid.pack()


	def units_print(self):
		for y in range(self.grid.height):
			for x in range(self.grid.width):
				if self.grid.map[y][x] == 1:
					self.canvas_grid.create_rectangle(x * self.horizontal_dist_grid,
																						y * self.vertical_dist_grid,
																						(x + 1) * self.horizontal_dist_grid,
																						(y + 1) * self.vertical_dist_grid, fill='black')
					self.canvas_grid.pack()

