from Grid import Grid as Grid_generator
from Agent import *
from tkinter import *
import time


class Protocol():
	def __init__(self, nb_hunter, nb_prey, time_limit, ratio, width_grid, height_grid, wall, id_protocol, experience, detection_range_prey, detection_range_hunter):
		self.nb_hunter = int(nb_hunter)
		self.nb_prey = int(nb_prey)
		self.width_grid = int(width_grid)
		self.height_grid = int(height_grid)
		self.wall = int(wall)
		self.ratio = int(ratio)
		self.detection_range_prey = int(detection_range_prey)
		self.detection_range_hunter = int(detection_range_hunter)
		self.id_protocol = int(id_protocol)
		self.experience = experience
		self.run = False
		self.done = False
		self.t = 0
		self.result = []
		self.score = [0, 0]
		self.time_limit = int(time_limit)
		self.num_party = 0
		self.grid = Grid_generator(self.height_grid, self.width_grid, self.wall)
		self.agents = self.agents_generator()
		self.launch_interface()
		self.print_wall()
		self.print_agents()
		#self.canvas_grid.mainloop()

	def launch(self):
		self.run = True
		if not self.experience.thread_onoff:
			self.experience.launch_thread()

	def next_step(self):
		if self.run:		
			self.t += 1
			for agent in self.agents:
				agent.next_mouvement(self)

			self.canvas_grid.delete('agent')
			self.sync_agents()
			self.print_agents()
			self.canvas_grid.update()
			self.is_done()

	def is_done(self):
		done = False
		done_time = False
		done_hunt = False
		if self.t >= self.time_limit:
			done_time = True
		for agent1 in self.agents:
			for agent2 in self.agents:
				if type(agent1) != type(agent2) and agent1.position_x == agent2.position_x and agent1.position_y == agent2.position_y:
					done_hunt = True
					if type(agent1) is Hunter:
						agent1.reward = 5
						agent2.reward = -5
					if type(agent2) is Hunter:
						agent2.reward = 5
						agent1.reward = -5

		if done_time and not done_hunt:
			self.score[0] += 1
			done = True
		if done_hunt:
			self.score[1] += 1
			done = True
		self.done = done

		if self.done:
			self.num_party += 1
			self.result.append([self.id_protocol, self.num_party,done_hunt,done_time,self.score])
			self.t = 0
			self.done = False
			self.replace_agents()


	def replace_agents(self):
		for agent in self.agents:
			if type(agent) is Prey:
				agent.temp_position_x = randint(0, int((self.width_grid - 1) / 4))
				agent.temp_position_y = randint(0, int((self.height_grid - 1) / 4))
			if type(agent) is Hunter:
				agent.temp_position_x = randint(int((self.width_grid - 1) / 1.25), self.width_grid - 1)
				agent.temp_position_y = randint(int((self.height_grid - 1) / 1.25), self.height_grid - 1)
		self.canvas_grid.delete('agent')
		self.sync_agents()
		self.print_agents()
		self.canvas_grid.update()

	def sync_agents(self):
		for agent in self.agents:
			agent.position_x = agent.temp_position_x
			agent.position_y = agent.temp_position_y

	def possibles_movements(self, x, y):
		if (0 <= x <= self.width_grid - 1 and 0 <= y <= self.height_grid - 1) and self.grid.map[y][x] != 1:
			return True
		else:
			return False


	def print_agents(self):
		for agent in self.agents:
			vertical_dist = self.grid_height_can / self.height_grid
			horizontal_dist = self.grid_width_can / self.width_grid
			color = "green"
			if type(agent) is Hunter:
				color = "red"
			if type(agent) is Prey:
				color = "blue"
			self.canvas_grid.create_rectangle(agent.position_x * horizontal_dist,
											agent.position_y * vertical_dist,
											(agent.position_x + 1) * horizontal_dist,
											(agent.position_y + 1) * vertical_dist, fill=color, tags='agent')

	def print_wall(self):
		for y in range(self.height_grid):
			for x in range(self.width_grid):
				vertical_dist = self.grid_height_can / self.height_grid
				horizontal_dist = self.grid_width_can / self.width_grid
				if self.grid.map[y][x] == 1:
					self.canvas_grid.create_rectangle(x * horizontal_dist,
					                         y * vertical_dist,
					                         (x + 1) * horizontal_dist,
					                         (y + 1) * vertical_dist, fill='black')

	def launch_interface(self):
		# dimension de la fenetre de pilotage
		self.window_width_protocol = 920 / self.ratio
		self.window_height_protocol = 1000 / self.ratio

		# création de la fenetre de pilotage
		self.window_protocol = Toplevel(self.experience.window_pilot)
		self.window_protocol.title('Protocol')
		geometry = str(int(self.window_width_protocol)) + 'x' + str(int(self.window_height_protocol))
		self.window_protocol.geometry(geometry)

		#Boutons de controles
		self.protocol_button_quit = Button(self.window_protocol, text="Quitter", command=self.quit)
		self.protocol_button_quit.grid(row=0,column=0)

		self.protocol_button_launch = Button(self.window_protocol, text="Lancer", command=self.launch)
		self.protocol_button_launch.grid(row=0,column=1)

		self.protocol_button_wait = Button(self.window_protocol, text="Pause", command=self.wait)
		self.protocol_button_wait.grid(row=0,column=2)

		self.protocol_button_reinit_agent = Button(self.window_protocol, text="Réinitialiser Agents", command=self.quit)
		self.protocol_button_reinit_agent.grid(row=0,column=3)

		self.protocol_button_log_agent = Button(self.window_protocol, text="Log Agents", command=self.log_agent)
		self.protocol_button_log_agent.grid(row=0,column=4)


		self.display_grid()

	def log_agent(self):
		for agent in self.agents:
			print(type(agent))
			print("position")
			print(agent.position_x,agent.position_y)
			agent.get_radar()
			print("radar")
			print(agent.radar)
			print("Partie : ",self.num_party)
			print("Score (P/H) : ",self.score)


	def display_grid(self):
		self.grid_width_can = self.window_width_protocol*0.9
		self.grid_height_can = self.window_height_protocol*0.9

		self.canvas_grid = Canvas(self.window_protocol, width=self.grid_width_can, height=self.grid_height_can, bg='grey')
		self.canvas_grid.grid(row=1, column=0, columnspan=5)



		# dislpay grid
		vertical_dist = self.grid_height_can / self.height_grid
		horizontal_dist = self.grid_width_can / self.width_grid
		# rows
		for y in range(self.height_grid):
			self.canvas_grid.create_line(0, (y + 1) * vertical_dist, self.grid_width_can, (y + 1) * vertical_dist)
			self.canvas_grid.grid(row=1, column=0, columnspan=5)
		# columns
		for x in range(self.width_grid):
			self.canvas_grid.create_line((x + 1) * horizontal_dist, 0, (x + 1) * horizontal_dist, self.grid_height_can)
			self.canvas_grid.grid(row=1, column=0, columnspan=5)


	def wait(self):
		self.run = False

	def quit(self):
		self.run = False  # to stop While in simulation()
		print(self.t)
		#print(self.result)
		self.window_protocol.destroy()



	def agents_generator(self):
	  agents = []
	  for p in range(self.nb_prey):
	      prey_x = randint(0, int((self.width_grid - 1) / 4))
	      prey_y = randint(0, int((self.height_grid - 1) / 4))
	      agents.append(Prey(prey_x, prey_y, self.grid, self.detection_range_prey))

	  for h in range(self.nb_hunter):
	      hunt_x = randint(int((self.width_grid - 1) / 1.25), self.width_grid - 1)
	      hunt_y = randint(int((self.height_grid - 1) / 1.25), self.height_grid - 1)
	      agents.append(Hunter(hunt_x, hunt_y, self.grid, self.detection_range_hunter))
	  return agents
