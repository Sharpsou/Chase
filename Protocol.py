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
		self.learn = True
		self.rand = True

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
		for agent in self.agents:
			agent.agents = self.agents
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
			for agent in self.agents:
				#agent.reward = agent.reward*self.t
				agent.remember()
			if self.done:
				self.done = False
				for agent in self.agents:
					if type(agent) is Hunter and self.done_hunt:
						#agent.memory_temp[][2] = agent.memory_temp[][2]*(self.time_limit-self.t)
						for r in agent.memory_temp:
							r[2] = r[2]*(self.time_limit-self.t)
					if type(agent) is Prey and self.done_time:
						#agent.memory_temp[][2] = agent.memory_temp[][2]*self.t
						for r in agent.memory_temp:
							r[2] = r[2]*self.t
					agent.memory = agent.memory + agent.memory_temp
					agent.memory_temp = []
					agent.memory = sorted(agent.memory,key=lambda l:l[2], reverse=True)
					agent.memory = agent.memory[:agent.memory_size]

	def is_done(self):
		replace_agent=[]
		done = False
		done_time = False
		done_hunt = False
		if self.t >= self.time_limit:
			done_time = True
			for agent in self.agents:
				if type(agent) is Hunter:
					replace_agent.append(agent)
		for agent1 in self.agents:
			for agent2 in self.agents:
				if type(agent1) != type(agent2) and agent1.position_x == agent2.position_x and agent1.position_y == agent2.position_y:
					done_hunt = True
					if type(agent1) is Hunter:
						agent1.reward = 5
						agent2.reward = -5
						replace_agent.append(agent2)

					if type(agent2) is Hunter:
						agent2.reward = 5
						agent1.reward = -5
						replace_agent.append(agent1)


		if done_time and not done_hunt:
			self.score[0] += 1
			done = True
		if done_hunt:
			self.score[1] += 1
			done = True
		self.done = done
		self.done_time = done_time
		self.done_hunt = done_hunt
		if self.done:
			self.num_party += 1
			self.result.append([self.id_protocol, self.num_party,done_hunt,done_time,self.score])
			self.t = 0
			self.replace_agents(replace_agent)


	def replace_agents(self,replace_agent):
		for agent in replace_agent:
			if type(agent) is Prey:
				agent.temp_position_x = randint(0, int((self.width_grid - 1) / 4))
				agent.temp_position_y = randint(0, int((self.height_grid - 1) / 4))
			if type(agent) is Hunter:
				agent.temp_position_x = randint(int((self.width_grid - 1) / 1.25), self.width_grid - 1)
				agent.temp_position_y = randint(int((self.height_grid - 1) / 1.25), self.height_grid - 1)
			if self.learn:
				agent.NN.decay_epsilon()

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

		self.protocol_button_reinit_agent = Button(self.window_protocol, text="Réinitialiser Agents", command=self.reinit_brain_agents)
		self.protocol_button_reinit_agent.grid(row=0,column=3)

		self.protocol_button_log_agent = Button(self.window_protocol, text="Log Agents", command=self.log_agent)
		self.protocol_button_log_agent.grid(row=0,column=4)

		self.protocol_button_learn = Button(self.window_protocol,text='Learn ON/OFF',command=self.active_learn)
		self.protocol_button_learn.grid(row=1,column=2)

		self.protocol_button_rand = Button(self.window_protocol,text='Aléatoire ON/OFF',command=self.active_rand)
		self.protocol_button_rand.grid(row=1,column=3)

		self.display_grid()

	def active_learn(self):
		if self.learn:
			self.learn = False
		else:
			self.learn = True
		for agent in self.agents:
			agent.NN.learn = self.learn

	def active_rand(self):
		if self.rand:
			self.rand = False
		else:
			self.rand = True


	def reinit_brain_agents(self):
		for agent in self.agents:
			agent.NN.shuffle_weights()
			agent.reward = 0
			agent.NN.epsilon = 1
		self.replace_agents(self.agents)
		self.score = [0, 0]

	def log_agent(self):
		for agent in self.agents:
			print(type(agent))
			print("position")
			print(agent.position_x,agent.position_y)
			print("radar")
			print(agent.radar)
			print("radar agent")
			print(agent.radar_agent)
			print("Partie : ",self.num_party)
			print("Score (P/H) : ",self.score)
			print(agent.radar_to_NN())
			print(agent.NN.epsilon)
			print(self.learn)
			print(self.rand)
			print(agent.NN.evaluate())
			# print('memory')
			# col = []
			# for r in agent.memory:
			# 	col.append(r[2])
			# print(col)
			# print('memory_temp')
			# col = []
			# for r in agent.memory_temp:
			# 	col.append(r[2])
			# print(col)
			# print("memory")
			# print(agent.memory)


	def display_grid(self):
		self.grid_width_can = self.window_width_protocol*0.9
		self.grid_height_can = self.window_height_protocol*0.9

		self.canvas_grid = Canvas(self.window_protocol, width=self.grid_width_can, height=self.grid_height_can, bg='grey')
		self.canvas_grid.grid(row=2, column=0, columnspan=5)



		# dislpay grid
		vertical_dist = self.grid_height_can / self.height_grid
		horizontal_dist = self.grid_width_can / self.width_grid
		# rows
		for y in range(self.height_grid):
			self.canvas_grid.create_line(0, (y + 1) * vertical_dist, self.grid_width_can, (y + 1) * vertical_dist)
			self.canvas_grid.grid(row=2, column=0, columnspan=5)
		# columns
		for x in range(self.width_grid):
			self.canvas_grid.create_line((x + 1) * horizontal_dist, 0, (x + 1) * horizontal_dist, self.grid_height_can)
			self.canvas_grid.grid(row=2, column=0, columnspan=5)


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
	      agents.append(Prey(prey_x, prey_y, self.grid, self.detection_range_prey,self.time_limit,self.t))

	  for h in range(self.nb_hunter):
	      hunt_x = randint(int((self.width_grid - 1) / 1.25), self.width_grid - 1)
	      hunt_y = randint(int((self.height_grid - 1) / 1.25), self.height_grid - 1)
	      agents.append(Hunter(hunt_x, hunt_y, self.grid, self.detection_range_hunter,self.time_limit,self.t))
	  return agents
