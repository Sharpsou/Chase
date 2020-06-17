from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.layers import Dropout
from random import *
import numpy as np



class NN:
	def __init__(self, learning_rate=0.1, epsilon_decay=0.99, memory_size=3000, batch_size=1000, agent=None):
		self.epsilon = 1
		self.epsilon_min = 0.01
		self.epsilon_decay = epsilon_decay
		self.action_size = 9
		self.learning_rate = learning_rate
		self.agent = agent
		self.state_size = ((self.agent.detection_range*2)+1)*((self.agent.detection_range*2)+1)*2
		self.batch_size = batch_size

		self.model = Sequential()
		self.model.add(Dense(int(self.state_size/2), input_dim=self.state_size, activation='relu'))
		self.model.add(Dense(int(16), activation='relu'))
		# self.model.add(Dropout(rate=0.2))
		# self.model.add(Dense(int(16), activation='relu'))
		# self.model.add(Dropout(rate=0.2))
		# self.model.add(Dense(int(16), activation='relu'))

		self.model.add(Dense(self.action_size, activation='relu'))
		self.model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate), metrics=['accuracy'])


	def decay_epsilon(self):
		self.epsilon *= self.epsilon_decay
		if self.epsilon < self.epsilon_min:
			self.epsilon = self.epsilon_min

	def predict(self,rand):
		value_in = self.agent.radar_to_NN()
		value_in = np.asarray([value_in])

		if rand and np.random.rand() <= self.epsilon:
			action = randrange(self.action_size)
			act_values = np.zeros(self.action_size)
			act_values[action] = 1
			return action, act_values
		else:
			# Predict
			#print(value_in)
			act_values = self.model.predict(value_in)
			action = np.argmax(act_values[0])
			act_values = np.zeros(self.action_size)
			act_values[action] = 1
			self.fit()
			return action, act_values

	def shuffle_weights(self, weights=None):
		if weights is None:
			weights = self.model.get_weights()
		weights = [np.random.permutation(w.flat).reshape(w.shape) for w in weights]
		# Faster, but less random: only permutes along the first dimension
		# weights = [np.random.permutation(w) for w in weights]
		self.model.set_weights(weights)

	def fit(self):
		batch_size = min(self.batch_size, len(self.agent.memory))
		train_set = sample(self.agent.memory,batch_size)

		inputs = np.zeros((batch_size, self.state_size))
		outputs = np.zeros((batch_size, self.action_size))

		for i, (state, action, reward) in enumerate(train_set):
			inputs[i] = state
			outputs[i] = action

		self.model.fit(inputs, outputs, epochs=1, verbose=1)