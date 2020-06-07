from tkinter import *
from Protocol import *

# XKIAN5
# SUJ00F

class Experience:
	def __init__(self, ratio=3):
		self.nb_protocol = 0
		self.thread_onoff = False
		self.time_sleep = 0.01
		self.launch_interface_experience(ratio)


	def launch_interface_experience(self, ratio):
		# dimension de la fenetre de pilotage
		self.ratio_pilot = ratio
		self.window_width_pilot = 1170 / ratio
		self.window_height_pilot = 830 / ratio
		self.protocols = []
		
		# création de la fenetre de pilotage
		self.window_pilot = Tk()
		self.window_pilot.title('Experience')
		geometry = str(int(self.window_width_pilot)) + 'x' + str(int(self.window_height_pilot))
		self.window_pilot.geometry(geometry)




		# definition des boutons et champs de saisi pour lancer les protocols
		# champs de saisi
		self.nb_prey = Entry(self.window_pilot)
		self.nb_hunter = Entry(self.window_pilot)
		self.width_grid = Entry(self.window_pilot)
		self.height_grid = Entry(self.window_pilot)
		self.ratio_grid = Entry(self.window_pilot)
		self.time_limit = Entry(self.window_pilot)
		self.wall = Entry(self.window_pilot)
		self.detection_range_hunter = Entry(self.window_pilot)
		self.detection_range_prey = Entry(self.window_pilot)

		self.nb_prey_txt = Label(self.window_pilot, text = 'Saisir nb proie : ')
		self.nb_hunter_txt = Label(self.window_pilot, text ='Saisir nb chasseur : ')
		self.width_grid_txt = Label(self.window_pilot, text ='Nb de case en X : ')
		self.height_grid_txt = Label(self.window_pilot, text = 'Nb de case en Y : ')
		self.ratio_grid_txt = Label(self.window_pilot, text ='Ratio grid : ')
		self.time_limit_txt = Label(self.window_pilot, text ='Time limit : ')
		self.wall_txt = Label(self.window_pilot, text = 'Nb de mur sur 10 cases : ')
		self.speed_txt = Label(self.window_pilot, text = 'Reglage de la vitesse')
		self.detection_range_hunter_txt = Label(self.window_pilot, text = 'Rayon detection chasseur : ')
		self.detection_range_prey_txt = Label(self.window_pilot, text = 'Rayon detection proie : ')
		


		# valeur par defaut
		self.nb_prey.insert(1, '1')
		self.nb_hunter.insert(1, '1')
		self.width_grid.insert(1, '10')
		self.height_grid.insert(1, '10')
		self.ratio_grid.insert(1, '2')
		self.time_limit.insert(1, '20')
		self.wall.insert(1, '1')
		self.detection_range_hunter.insert(1, '2')
		self.detection_range_prey.insert(1, '2')
		
		# boutons de lancement et quit  
		self.button_pilot_protocol = Button(self.window_pilot, text="Lancer simulation", command=self.launch_protocol)
		self.button_pilot_quit = Button(self.window_pilot, text="Quit", command=self.quit)

		self.button_pilot_speedup = Button(self.window_pilot, text="+", command=self.speedup)
		self.button_pilot_speeddown = Button(self.window_pilot, text="-", command=self.speeddown)
		
		# pack button and entry

		self.nb_prey_txt.grid(row=0,column=0)
		self.nb_hunter_txt.grid(row=1,column=0)
		self.width_grid_txt.grid(row=2,column=0)
		self.height_grid_txt.grid(row=3,column=0)
		self.ratio_grid_txt.grid(row=4,column=0)
		self.time_limit_txt.grid(row=5,column=0)
		self.wall_txt.grid(row=6,column=0)

		self.nb_prey.grid(row=0,column=1)
		self.nb_hunter.grid(row=1,column=1)
		self.width_grid.grid(row=2,column=1)
		self.height_grid.grid(row=3,column=1)
		self.ratio_grid.grid(row=4,column=1)
		self.time_limit.grid(row=5,column=1)
		self.wall.grid(row=6,column=1)

		self.detection_range_hunter_txt.grid(row=7,column=0)
		self.detection_range_hunter.grid(row=7,column=1)
		self.detection_range_prey_txt.grid(row=8,column=0)
		self.detection_range_prey.grid(row=8,column=1)


		self.button_pilot_protocol.grid(row=10,column=1)
		self.button_pilot_quit.grid(row=10,column=0)

		self.button_pilot_speeddown.grid(row=9,column=1)
		self.speed_txt.grid(row=9,column=0)
		self.button_pilot_speedup.grid(row=9,column=2)

		

		# lancement de la boucle
		self.window_pilot.mainloop()
		
	def speedup(self):
		self.time_sleep *= 0.2

	def speeddown(self):
		self.time_sleep *= 5

	def quit(self):
		self.window_pilot.destroy()
		self.thread_onoff = False
		sys.exit()

	def launch_thread(self):
		self.thread_onoff = True
		while self.thread_onoff:
			all_run = False
			for protocol in self.protocols:
				if protocol.run:
					all_run = True
					protocol.next_step()
			self.thread_onoff = all_run
			time.sleep(self.time_sleep)


	def launch_protocol(self):
		#self.thread_onoff = False
		print('nb proie = ',self.nb_prey.get(),'nb chasseur = ',self.nb_hunter.get())
		print('largeur = ',self.width_grid.get(),'hauteur = ',self.height_grid.get())
		print('ratio = ',self.ratio_grid.get())

		self.protocols.append(Protocol(nb_hunter=self.nb_hunter.get(), 
										nb_prey=self.nb_prey.get(), 
										ratio=self.ratio_grid.get(), 
										time_limit=self.time_limit.get(),
										width_grid=self.width_grid.get(),
										height_grid=self.height_grid.get(),
										wall=self.wall.get(),
										id_protocol=self.nb_protocol,
										experience=self,
										detection_range_prey=self.detection_range_prey.get(),
										detection_range_hunter=self.detection_range_hunter.get()))
		self.nb_protocol += 1		
		for p in self.protocols:
			print(p.grid.map)
			print(p.agents)
			print("Id ",p.id_protocol," : ",p.run)
		#self.launch_thread()
		





test = Experience()

