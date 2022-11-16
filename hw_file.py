#!/usr/bin/env python3
import math
import random

gamma = 0.9
tolerance = 0.001
# probability of failure
# alpha = 0.15
# p_success = 1 - alpha


policy_hist = {}


class MDP:

	def __init__(self):
		self.policy = {}
		self.state_values = {}
		self.probabilities = {}
		self.chance_nodes = ['J','G']
		self.decision_nodes = ['B','C','D','E','F','H','I','K','L','M','N','P']
		self.terminal_nodes = ['A','Q']
		self.all_states = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','P','Q']
		self.alpha = 0.15
		self.p_success = 0.85

		self.rewards = {
			'A' : 11,
			'B' : -1,
			'C' : -1,
			'D' : -1,
			'E' : -1, 
			'F' : -1, 
			'G' : 4, 
			'H' : -1, 
			'I' : -1, 
			'J' : 4, 
			'K' : -1, 
			'L' : -1, 
			'M' : -1, 
			'N' : -1, 
			'P' : -1, 
			'Q' : -11 
		}


		self.neighbors_directed = {
			'A' : [],
			'B' : ['A', 'C', 'F'],
			'C' : ['B', 'G', 'D'],
			'D' : ['C', 'H'],
			'E' : ['A', 'F', 'I'],
			'F' : ['E', 'B', 'G', 'J'],
			'G' : ['F', 'C', 'H', 'K'],
			'H' : ['D', 'G', 'L'],
			'I' : ['E', 'J', 'M'],
			'J' : ['I', 'F', 'K', 'N'],
			'K' : ['J', 'G', 'L', 'P'],
			'L' : ['K', 'H', 'Q'],
			'M' : ['I', 'N'],
			'N' : ['M', 'J', 'P'],
			'P' : ['N', 'K', 'Q'],
			'Q' : []
		}

		# for the hw only
		self.self_loops = True
		self.against_wall = ['A','B','C','D','E','H','I','L','M','N','P','Q']


	def make_random_policy(self):
		for letter in self.all_states:

			print(letter)
			letters_neighbors = self.neighbors_directed[letter]

			# if not letters_neighbors:
			if letter in self.terminal_nodes:
				# we know it's a terminal node, so leave it empty
				self.policy[letter] = None

			elif letter in self.chance_nodes:
				self.policy[letter] = None

			else:
				#otherwise pick a random neighbor to assign
				choice = random.choice(letters_neighbors)
				print("initially setting policy for %s -> %s" % (letter, choice))
				self.policy[letter] = choice

		# for my logging and debugging, add it to the policy hist
		for s,val in self.policy.items():
			policy_hist[s] = [val]


	def set_initial_values(self):
		for letter in self.all_states:
			self.state_values[letter] = 0


	def set_up_probabilities(self):
		for letter in self.neighbors_directed.keys():
			print("letter : %s" % letter)

			# TERMINALS
			if letter in self.terminal_nodes:
				self.probabilities[letter] = [1]

			# CHANCE NODES
			if letter in self.chance_nodes:
				# split evenly among directed children
				equal_chance_nodes = self.neighbors_directed[letter].copy()

				# for the hw only
				if self.self_loops:
					if letter in self.against_wall:
						equal_chance_nodes.append(letter)

				split = len(equal_chance_nodes)

				# ie, make a list like 
				#   [1/4, 1/4, 1/4, 1/4]
				self.probabilities[letter] = [1/split] * split

			# DECISION NODES
			if letter in self.decision_nodes:

				adjacent_nodes = self.neighbors_directed[letter].copy()

				# for the hw only
				if self.self_loops:
					if letter in self.against_wall:
						adjacent_nodes.append(letter)

				num_adjacent = len(adjacent_nodes)

				# look up what the policy should be
				choice_direction = self.policy[letter]

				# initially, set probabilities to 0
				self.probabilities[letter] = [0] * num_adjacent

				# fill in top choice gets highest prob
				self.probabilities[letter][0] = self.p_success

				# rest of them get distributed evenly
				split = self.alpha/(num_adjacent - 1)

				# assigns index 1... end with the equal split of p_fail
				for z in range(1,num_adjacent):
					
					self.probabilities[letter][z] = split
					# print("z:%s assign p_fail:%s " % (z, split))


			print(self.probabilities[letter])
		


	def _argmax(self, state):

		largest = float('-inf')
		next_policy = None

		for adjacent_state in self.neighbors_directed[state]:
			# print("adj -> %s" % adjacent_state)

			if self.state_values[adjacent_state] > largest:

				# print("%s > %s" % (self.state_values[adjacent_state], largest))

				largest = self.state_values[adjacent_state]
				next_policy = adjacent_state
			else:
				pass
				# print("not larger // %s vs %s" % (self.state_values[adjacent_state], largest))

		return next_policy


	def _value_iteration_inner(self, state_value_dict):

		pi_current_values = state_value_dict.copy()
		pi_state_values = {}

		for state, curr_val in state_value_dict.items():


		# for state in state_names:

			print("working on state %s" % state)
			# for all of them, they are just assigned their iterative value
			pi_value = self.rewards[state]

			print("\n")

			# TERMINAL 
			if state in self.terminal_nodes:
				pi_state_values[state] = pi_value
				# print("value for terminal node %s" % pi_value)

				print("%s = %s" % (state,pi_value))


			# CHANCE
			elif state in self.chance_nodes:
				# get the neighbors of chance node
				restof_nodes = self.neighbors_directed[state].copy()
				transition_states = restof_nodes

				# get the transition probabilities of the chance node
				transition_likelihoods = self.probabilities[state]

				if len(transition_likelihoods) != len(transition_states):
					print("there is a huge problem here...")

				# debugging
				print("%s = %s " % (state,pi_value), end="")

				for y in range(len(transition_states)):

					adjacent_state_name = transition_states[y]

					# this should be ok to pull from state_values 
					# because they won't be updated until the convergence is finished
					# transitional_value = self.state_values[transition_states[y]]

					# ^ I DONT WANT THAT, you need the current iterative value
					# transitional_value = curr_val
					# dont want that either, thats current value of the curent equation 
					transitional_value = pi_current_values[adjacent_state_name]


					additive_value = gamma * transition_likelihoods[y] * transitional_value

					pi_value+= additive_value
					pi_state_values[state] = pi_value

					# debugging
					print("+ (%s)*(%s)*(%s) " % (gamma, transition_likelihoods[y], adjacent_state_name), end="")

					# print("\ty:%s, to_state:%s, transitional_value:%s, likelihood:%s == additive_value:%s" % (y, transition_states[y], transitional_value, transition_likelihoods[y], additive_value))
					# print("\tnew value: %s" % pi_value)

			elif state in self.decision_nodes:

				# debugging
				print("%s = %s " % (state,pi_value), end="")

				to_node = self.policy[state]
				# print("\tshould go to node %s" % to_node)

				restof_nodes = self.neighbors_directed[state].copy()
				restof_nodes.remove(to_node)

				# for the hw only
				if self.self_loops:
					if state in self.against_wall:
						restof_nodes.append(state)

				transition_states = []
				transition_states.append(to_node)
				transition_states.extend(restof_nodes)

				# print("\t other nodes: %s" % restof_nodes)

				transition_likelihoods = self.probabilities[state]

				if len(transition_likelihoods) != len(transition_states):
					print("there is a huge problem here...")


				for y in range(len(transition_states)):

					# transitional_value = self.state_values[transition_states[y]]
					# ^ dont want that, i want the current iterative value

					# transitional_value = curr_val
					# dont want that either, thats current value of the curent equation 
					adjacent_state_name = transition_states[y]
					transitional_value = pi_current_values[adjacent_state_name]

					additive_value = gamma * transition_likelihoods[y] * transitional_value

					pi_value+= additive_value
					pi_state_values[state] = pi_value

					# debugging
					print("+ (%s)*(%s)*(%s) " % (gamma, transition_likelihoods[y], adjacent_state_name), end="")
					# print("\t+ (%s)*(%s)*(%s) " % (gamma, transition_likelihoods[y], transitional_value), end="")

					# print("\ty:%s, to_state:%s, transitional_value:%s, likelihood:%s == additive_value:%s" % (y, transition_states[y], transitional_value, transition_likelihoods[y], additive_value))
					# print("\tnew value: %s" % pi_value)

			print("\n")


		print(pi_state_values)
		# return a dictionary
		return pi_state_values

		'''
			a single iteration of the value computation

		return this iteration's variable values
		'''

	def value_iteration(self):
		# set the convergence to false
		# compute appropriate deltas and compare for convergence
		# upon convergence, return and set the new state_values
		#  for the mdp class

		# make temp of the values 
		pi_values = self.state_values.copy()

		# compare what is the deal with these values initially
		print("\n")
		for k,v in pi_values.items():
			print("%s:%s " % (k,v), end="")
		print("\n")

		converge=False
		x=0

		while not converge:
			x+= 1
			print("\nIteration %s:" % x)

			if x == 100:
				break

			delta = 0


			temp_pi_values = pi_values

			if temp_pi_values == self.state_values:
				print("yes, copy is first iteration")
			else:
				print("iterating with different pi_values")


			pi_values = self._value_iteration_inner(pi_values)


			# then we will compare the values between:
			# prev_pi_values, iteration_pi_values
			# get the deltas, check if we converge

			print("\n")
			for state,value in pi_values.items():

				delta = max(delta,( abs(temp_pi_values[state] - value) ))
				print(" delta %s" % delta, end="")

			print("delta :%s \n" % delta)

			if delta < tolerance:
				print("I converge after %s iterations\n" % x)
				converge = True

			# # this is an experiment and i shouldnt keep this here
			# print("running with SINGLE ITERATION ONLY as EXPERIMENT")
			# converge=True


		# compare what is the deal with these values initially
		print("\nOLD values before converge:")
		for k,v in self.state_values.items():
			print("%s:%s " % (k,v), end="")
		print("\n")


		self.state_values = pi_values.copy()

		# compare what is the deal with these values initially
		print("\nNew values after converge:")
		for k,v in self.state_values.items():
			print("%s:%s " % (k,v), end="")
		print("\n")


		return converge



	def recalculate_policy(self):

		# for every node's adjacency, pick the one that has the highest value
		# use that as the new policy assignment
		
		# for state in self.neighbors_directed.keys():
		# for state in self.policy.keys():
		counter = 0
		for state, former_policy in self.policy.items():


			print("reassigning policy for state: %s. previously -> %s" % (state, former_policy))

			# get the arg max
			to_state = self._argmax(state)

			if former_policy != to_state:
				counter+=1

			self.policy[state] = to_state
			print("new policy ---> %s" % to_state)




		print("new policy:")
		for k,v in self.policy.items():
			print("%s --> %s" % (k,v))
			policy_hist[k].append(v)


		return counter


	def policy_iteration(self):

		# M.value_iteration()
		# policy_change = M.recalculate_policy()

		policy_changing = True

		y = 0

		while policy_changing:

			y+=1
			if y == 100:
				print("BROKE OUT OF LOOP, limited y value, extend this??")
				break

			self.value_iteration()
			policy_changes = M.recalculate_policy()


			if policy_changes == 0:
				policy_changing = False


		print("finished after %s iterations" % y)


'''
# i liked this pseudocode here:
https://medium.com/@ngao7/markov-decision-process-value-iteration-2d161d50a6ff

while not converge
	delta = 0
	for s in S:
		temp = v_s
		v_s = r_s + gamma * max (P * v(s'))
		delta = max(delta, abs(temp - v_s))
	if delta < tolerance
		converge = true

	for s in S:
		pi_star_s = argmax SUM(P*V(s'))
'''



if __name__ == '__main__':

	M = MDP()

	# set initial policy is random
	M.make_random_policy()
	M.set_initial_values()


	# make the equations
	M.set_up_probabilities()

	M.policy_iteration()





	for k,v in policy_hist.items():
		print("%s : %s" % (k,v))


	for state, final_val in M.state_values.items():
		print("%s -> %s" % (state, final_val))












	





