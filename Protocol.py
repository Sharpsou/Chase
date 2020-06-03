from Grid import Grid as Grid_generator
from Agent import *
from tkinter import *


class Protocol:
	def __init__(self, nb_hunter, nb_prey, time_limit, ratio, width_grid, height_grid, wall, id_protocol):
		self.nb_hunter = int(nb_hunter)
		self.nb_prey = int(nb_prey)
		self.width_grid = int(width_grid)
		self.height_grid = int(height_grid)
		self.wall = int(wall)
		self.ratio = int(ratio)
		self.id_protocol = int(id_protocol)
		self.run = True
		self.done = False
		self.t = 0
		self.result = []
		self.score = [0, 0]
		self.time_limit = time_limit
		self.num_party = 0
		self.grid = Grid_generator(self.height_grid, self.width_grid, self.wall)
		self.agents = self.agents_generator()
		self.launch_interface(ratio=self.ratio)


	def launch_interface(self, ratio=3):
		# dimension de la fenetre de pilotage
		self.ratio_protocol = ratio
		self.window_width_protocol = 920 / self.ratio_protocol
		self.window_height_protocol = 1000 / self.ratio_protocol

		# création de la fenetre de pilotage
		self.window_protocol = Tk()
		self.window_protocol.title('Protocol')
		geometry = str(int(self.window_width_protocol)) + 'x' + str(int(self.window_height_protocol))
		self.window_protocol.geometry(geometry)

		#Boutons de controles
		self.protocol_button_quit = Button(self.window_protocol, text="Quitter", command=self.quit)
		self.protocol_button_quit.grid(row=0,column=0)

		self.protocol_button_launch = Button(self.window_protocol, text="Lancer", command=self.quit)
		self.protocol_button_launch.grid(row=0,column=1)

		self.protocol_button_reinit_agent = Button(self.window_protocol, text="Réinitialiser Agents", command=self.quit)
		self.protocol_button_reinit_agent.grid(row=0,column=2)

		self.protocol_button_log_agent = Button(self.window_protocol, text="Log Agents", command=self.quit)
		self.protocol_button_log_agent.grid(row=0,column=3)

		self.display_grid()

	def display_grid(self):
		grid_width_can = self.window_width_protocol*0.9
		grid_height_can = self.window_height_protocol*0.9

		self.canvas_grid = Canvas(self.window_protocol, width=grid_width_can, height=grid_height_can, bg='grey')
		self.canvas_grid.grid(row=1, column=0, columnspan=5)

		# dislpay grid
		vertical_dist = grid_height_can / self.height_grid
		horizontal_dist = grid_width_can / self.width_grid
		# rows
		for y in range(self.height_grid):
			self.canvas_grid.create_line(0, (y + 1) * vertical_dist, grid_width_can, (y + 1) * vertical_dist)
			self.canvas_grid.grid(row=1, column=0, columnspan=5)
		# columns
		for x in range(self.width_grid):
			self.canvas_grid.create_line((x + 1) * horizontal_dist, 0, (x + 1) * horizontal_dist, grid_height_can)
			self.canvas_grid.grid(row=1, column=0, columnspan=5)


	def quit(self):
		self.run = False  # to stop While in simulation()
		self.window_protocol.destroy()


	def agents_generator(self):
	  agents = []
	  for p in range(self.nb_prey):
	      prey_x = randint(0, int((self.width_grid - 1) / 2))
	      prey_y = randint(0, int((self.height_grid - 1) / 2))
	      agents.append(Prey(prey_x, prey_y))

	  for h in range(self.nb_hunter):
	      hunt_x = randint(int((self.width_grid - 1) / 2), self.width_grid - 1)
	      hunt_y = randint(int((self.height_grid - 1) / 2), self.height_grid - 1)
	      agents.append(Hunter(hunt_x, hunt_y))
	  return agents
