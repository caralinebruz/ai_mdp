#!/usr/bin/env python3
import math
import random


class MDP:

	def __init__(self, gamma, tolerance, max_iterations, minimize_values, props):
		self.policy = {}
		self.state_values = {}
		self.probabilities = {}
		self.policy_hist = {}

		self.tolerance = tolerance
		self.gamma = gamma
		self.max_iterations = max_iterations
		self.minimize_values = minimize_values

		self.given_probabilities = props['probabilities']
		self.rewards = props['rewards']
		self.chance_nodes = props['chance_nodes']
		self.decision_nodes = props['decision_nodes']
		self.terminal_nodes = props['terminal_nodes']
		self.all_states = props['all_states']
		self.neighbors_directed = props['neighbors_directed']
		

	def make_random_policy(self):
		'''Picks from adjancent edges at random
		
			*Returns: A random policy
		'''
		for letter in self.all_states:

			# if not letters_neighbors:
			if letter in self.terminal_nodes:
				self.policy[letter] = None
				self.neighbors_directed[letter] = []

			elif letter in self.chance_nodes:
				self.policy[letter] = None

			else:
				#otherwise pick a random neighbor to assign
				letters_neighbors = self.neighbors_directed[letter]
				choice = random.choice(letters_neighbors)
				self.policy[letter] = choice

		# for my logging and debugging, add it to the policy hist
		for s,val in self.policy.items():
			self.policy_hist[s] = [val]


	def set_initial_values(self):
		# initialize values as 0, initially
		for letter in self.all_states:
			self.state_values[letter] = 0


	def set_up_probabilities(self):
		'''Based on what was given in the input file

			*Returns: distributed probabilities across all edge space (v')
		'''
		for letter in self.neighbors_directed.keys():

			# TERMINALS
			if letter in self.terminal_nodes:
				self.probabilities[letter] = [1]

			# CHANCE NODES
			if letter in self.chance_nodes:

				adjacent_nodes = self.neighbors_directed[letter].copy()
				nodes_probabilities = self.given_probabilities[letter].copy()
				self.probabilities[letter] = nodes_probabilities
				
			# DECISION NODES
			if letter in self.decision_nodes:

				adjacent_nodes = self.neighbors_directed[letter].copy()
				num_adjacent = len(adjacent_nodes)

				# look up what the policy should be
				choice_direction = self.policy[letter]

				# initially, set probabilities to 0
				self.probabilities[letter] = [0] * num_adjacent

				# fill in top choice gets highest prob
				p_success = self.given_probabilities[letter][0]
				p_fail = 1 - p_success
				self.probabilities[letter][0] = p_success

				# if p_success ==1 then there is nothing to distribute
				if p_success < 1:
					split = p_fail/(num_adjacent - 1)

					# assigns index 1... end with the equal split of p_fail
					for z in range(1,num_adjacent):
						self.probabilities[letter][z] = split
		


	def _argmax(self, state):
		'''Performs argmin / argmax of inputs
		
			*Returns: The next policy
		'''
		if not self.minimize_values:
			largest = float('-inf')
			next_policy = None

			for adjacent_state in self.neighbors_directed[state]:

				if self.state_values[adjacent_state] > largest:
					# print("%s > %s" % (self.state_values[adjacent_state], largest))
					largest = self.state_values[adjacent_state]
					next_policy = adjacent_state

		else:
			smallest = float('inf')
			next_policy = None

			for adjacent_state in self.neighbors_directed[state]:

				if self.state_values[adjacent_state] < smallest:
					# print("%s < %s" % (self.state_values[adjacent_state], smallest))
					smallest = self.state_values[adjacent_state]
					next_policy = adjacent_state


		return next_policy


	def _value_iteration_inner(self, state_value_dict):
		'''Performs a single iteration of the values

			*Returns: Intermediate values
		'''
		pi_current_values = state_value_dict.copy()
		pi_state_values = {}

		for state, curr_val in state_value_dict.items():

			pi_value = self.rewards[state]

			# TERMINAL 
			if state in self.terminal_nodes:
				pi_state_values[state] = pi_value

			# CHANCE
			elif state in self.chance_nodes:
				# get the neighbors of chance node
				restof_nodes = self.neighbors_directed[state].copy()
				transition_states = restof_nodes

				# get the transition probabilities of the chance node
				transition_likelihoods = self.probabilities[state]

				if len(transition_likelihoods) != len(transition_states):
					print("there is a huge problem here...")


				for y in range(len(transition_states)):

					adjacent_state_name = transition_states[y]
					transitional_value = pi_current_values[adjacent_state_name]
					additive_value = self.gamma * transition_likelihoods[y] * transitional_value

					pi_value+= additive_value
					pi_state_values[state] = pi_value

					# debugging
					# print("+ (%s)*(%s)*(%s) " % (self.gamma, transition_likelihoods[y], adjacent_state_name), end="")

			# DECISION 
			elif state in self.decision_nodes:
				to_node = self.policy[state]

				restof_nodes = self.neighbors_directed[state].copy()
				restof_nodes.remove(to_node)

				transition_states = []
				transition_states.append(to_node)
				transition_states.extend(restof_nodes)

				transition_likelihoods = self.probabilities[state]

				if len(transition_likelihoods) != len(transition_states):
					print("there is a huge problem here...")


				for y in range(len(transition_states)):

					adjacent_state_name = transition_states[y]
					transitional_value = pi_current_values[adjacent_state_name]
					additive_value = self.gamma * transition_likelihoods[y] * transitional_value

					pi_value+= additive_value
					pi_state_values[state] = pi_value

					# debugging
					# print("+ (%s)*(%s)*(%s) " % (self.gamma, transition_likelihoods[y], adjacent_state_name), end="")


		return pi_state_values


	def value_iteration(self):
		# set the convergence to false
		# compute appropriate deltas and compare for convergence
		# upon convergence, return and set the new state_values
		#  for the mdp class
		pi_values = self.state_values.copy()
		converge=False
		x=0

		while not converge:
			x+= 1
			# print("\nIteration %s:" % x)

			if x == self.max_iterations:
				break

			delta = 0
			temp_pi_values = pi_values

			# do the value iteration
			pi_values = self._value_iteration_inner(pi_values)

			for state,value in pi_values.items():
				delta = max(delta,( abs(temp_pi_values[state] - value) ))

			# evaluate our stopping criteria
			if delta < self.tolerance:
				converge = True


		self.state_values = pi_values.copy()
		return converge


	def recalculate_policy(self):
		# for every node's adjacency, pick the one that has the highest value
		# use that as the new policy assignment
		
		# for state in self.neighbors_directed.keys():
		# for state in self.policy.keys():
		counter = 0
		for state, former_policy in self.policy.items():

			# get the arg max
			to_state = self._argmax(state)

			if former_policy != to_state:
				counter+=1

			self.policy[state] = to_state

		# print("new policy:")
		# for k,v in self.policy.items():
		# 	print("%s --> %s" % (k,v))
		# 	self.policy_hist[k].append(v)

		return counter


	def policy_iteration(self):
		''' Evaluate if we should stop policy iteration
		'''
		policy_changing = True
		y = 0

		while policy_changing:
			y+=1
			if y == self.max_iterations:
				break

			self.value_iteration()
			policy_changes = self.recalculate_policy()

			if policy_changes == 0:
				policy_changing = False

		# print("finished after %s iterations" % y)



