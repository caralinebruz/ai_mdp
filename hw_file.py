#!/usr/bin/env python3
import math
import random

A = 0
B = 0
C = 0
D = 0
E = 0 
F = 0 
G = 0 
H = 0 
I = 0 
J = 0 
K = 0 
L = 0 
M = 0 
N = 0 
P = 0 
Q = 0 
T = 0

A_Temp = 0
B_Temp = 0
C_Temp = 0
D_Temp = 0
E_Temp = 0 
F_Temp = 0 
G_Temp = 0 
H_Temp = 0 
I_Temp = 0 
J_Temp = 0 
K_Temp = 0 
L_Temp = 0 
M_Temp = 0 
N_Temp = 0 
P_Temp = 0 
Q_Temp = 0 
T_Temp = 0

tolerance = 0.001
# probability of failure
alpha = 0.15
p_success = 1 - alpha


# TERMINAL NODES R(s) given
VA = 11
VQ = -11


# CHANCE NODES, R(s) = +4
# i, f, k, n
VJ = 4 + .25*I + .25*F + .25*K + .25*N
# f, c, h, k
VG = 4 + .25*F + .25*C + .25*H + .25*K



# DECISION NODES, R(s) = -1
# a, f, c, b
VB = -1 + .25*A + .25*F + .25*C + .25*B

# b, g, d, c
VC = -1 + .25*B + .25*G + .25*D + .25*C

# c, d, h
VD = -1 + .33333*C + .33333*D + .33333*H

# a, f, i, e
VE = -1 + .25*A + .25*F + .25*I + .25*E

# e, b, g, j
VF = -1 + .25*E + .25*B + .25*G + .25*J

# d, l, g, h
VH = -1 + .25*D + .25*L + .25*G + .25*H

# e, j, m, i
VI = -1 + .25*E + .25*J + .25*M + .25*I

# j, g, l, p
VK = -1 + .25*J + .25*G + .25*L + .25*P

# k, h, q, l
VL = -1 + .25*K + .25*H + .25*Q + .25*L

# i, n, m
VM = -1 + .33333*I + .33333*N + .33333*M

# m, j, p, n
VN = -1 + .25*M + .25*J + .25*P + .25*N 

# n, k, q, p
VP = -1 + .25*N + .25*K + .25*Q + .25*P



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
		for letter in alphabet:

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
				self.probabilities[letter][0] = p_success

				# rest of them get distributed evenly
				split = alpha/(num_adjacent - 1)

				# assigns index 1... end with the equal split of p_fail
				for z in range(1,num_adjacent):
					
					self.probabilities[letter][z] = split
					# print("z:%s assign p_fail:%s " % (z, split))


			print(self.probabilities[letter])


	def calculate_once(self):
	
		print("CALC SUBROUTINE")


		### NOTE, i need to add convergence here, i dont do more than 1 iteration.


		# make temp of the values 
		pi_values = self.state_values.copy()

		# compare what is the deal with these values initially
		print("\n")
		for k,v in pi_values.items():
			print("%s:%s " % (k,v), end="")
		print("\n")



		for state in self.all_states:

			print("working on state: %s" % state)

			# make a backup copy of the value
			temp = pi_values[state]
			# for all of them, they are just assigned their iterative value
			value = Rewards[state]

			# dont need to do anything else for terminal 
			if state in self.terminal_nodes:
				pi_values[state] = value
				print("\tnew value: %s" % value)



			if state in self.decision_nodes:

				to_node = self.policy[state]
				print("\tshould go to node %s" % to_node)

				restof_nodes = self.neighbors_directed[state].copy()
				restof_nodes.remove(to_node)
				# print("oringial resof+nodes %s" % restof_nodes)

				# for the hw only
				if self.self_loops:
					if state in self.against_wall:
						restof_nodes.append(state)

				transition_states = []
				transition_states.append(to_node)
				transition_states.extend(restof_nodes)

				print("\t other nodes: %s" % restof_nodes)

				transition_likelihoods = self.probabilities[state]

				if len(transition_likelihoods) != len(transition_states):
					print("there is a huge problem here...")


				for y in range(len(transition_states)):
					transitional_value = self.state_values[transition_states[y]]
					additive_value = gamma * transition_likelihoods[y] * transitional_value

					value+= additive_value
					pi_values[state] = value

					print("\ty:%s, to_state:%s, transitional_value:%s, likelihood:%s == additive_value:%s" % (y, transition_states[y], transitional_value, transition_likelihoods[y], additive_value))
					print("\tnew value: %s" % value)


			if state in self.chance_nodes:

				# J and G wont have self loops in the HW, so i wont write it now
				# j and g are internal nodes without any self loops

				restof_nodes = self.neighbors_directed[state].copy()

				transition_states = restof_nodes
				transition_likelihoods = self.probabilities[state]
				if len(transition_likelihoods) != len(transition_states):
					print("there is a huge problem here...")

				for y in range(len(transition_states)):
					transitional_value = self.state_values[transition_states[y]]
					additive_value = gamma * transition_likelihoods[y] * transitional_value

					value+= additive_value
					pi_values[state] = value

					print("\ty:%s, to_state:%s, transitional_value:%s, likelihood:%s == additive_value:%s" % (y, transition_states[y], transitional_value, transition_likelihoods[y], additive_value))
					print("\tnew value: %s" % value)


		# at the end, you'll ave the values for each node? what do i do with it?
		for k,v in pi_values.items():
			print("%s:%s " % (k,v), end="")
		print("\n")

		# at the end, update the overall state values with the iteration values??? or should i only do it after they converged?
		self.state_values = pi_values
				


	def _argmax(self, state):

		largest = float('-inf')
		next_policy = None

		for adjacent_state in self.neighbors_directed[state]:
			print("adj -> %s" % adjacent_state)

			if self.state_values[adjacent_state] > largest:

				print("%s > %s" % (self.state_values[adjacent_state], largest))

				largest = self.state_values[adjacent_state]
				next_policy = adjacent_state
			else:
				print("not larger // %s vs %s" % (self.state_values[adjacent_state], largest))

		return next_policy



	def recalculate_policy(self):

		# for every node's adjacency, pick the one that has the highest value
		# use that as the new policy assignment
		
		# for state in self.neighbors_directed.keys():
		# for state in self.policy.keys():
		for state, former_policy in self.policy.items():

			print("reassigning policy for state: %s. previously -> %s" % (state, former_policy))

			# get the arg max
			to_state = self._argmax(state)

			self.policy[state] = to_state

			print("new policy ---> %s" % to_state)




		print("new policy:")
		for k,v in self.policy.items():
			print("%s --> %s" % (k,v))







	# for letter in Neighbors_Directed.keys():

	# 	# if policy[letter] is None: # or if letter in terminals
	# 	if letter in terminal_nodes:
	# 		Value = Rewards[letter]

	# 	elif letter in chance_nodes:
	# 		# split evenly among directed children
	# 		equal_chance_nodes = Neighbors_Directed[letter]
	# 		Value = Rewards[letter]

	# 		split = len(equal_chance_nodes)
	# 		for adjacent_possibility in equal_chance_nodes:
	# 			Value += ( gamma * (1/split) * adjacent_possibility)




# supposed to converge to: T=10, A=7, B=6, C=5

# converge = False

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
# while not converge


def VI(A,B,C,D,E,F,G,H,I,J,K,L,M,N,P,Q):

	print("A:%s, B:%s, C:%s, D:%s, E:%s, F:%s, G:%s, H:%s, I:%s, J:%s, K:%s, L:%s, M:%s, N:%s, P:%s, Q:%s" % (A,B,C,D,E,F,G,H,I,J,K,L,M,N,P,Q))
	print()

	VA = 3
	VQ = 3
	VB = -2 + .25*A + .25*F + .25*C + .25*B
	VC = -2 + .25*B + .25*G + .25*D + .25*C
	VD = -2 + .333*C + .333*D + .333*H
	VE = -2 + .25*A + .25*F + .25*I + .25*E
	VF = -2 + .25*E + .25*B + .25*G + .25*J
	VG = -2 + .25*F + .25*C + .25*H + .25*K
	VH = -2 + .25*D + .25*L + .25*G + .25*H
	VI = -2 + .25*E + .25*J + .25*M + .25*I
	VJ = -2 + .25*I + .25*F + .25*K + .25*N
	VK = -2 + .25*J + .25*G + .25*L + .25*P
	VL = -2 + .25*K + .25*H + .25*Q + .25*L
	VM = -2 + .333*I + .333*N + .333*M
	VN = -2 + .25*M + .25*J + .25*P + .25*N 
	VP =  -2 + .25*N + .25*K + .25*Q + .25*P

	return VA, VB, VC, VD, VE, VF, VG, VH, VI, VJ, VK, VL, VM, VN, VP, VQ


alphabet = [
'A','B','C','D','E','F','G','H','I','J','K','L','M','N','P','Q'
]

temps = [
A_Temp, B_Temp, C_Temp, D_Temp, E_Temp, F_Temp, G_Temp, H_Temp, I_Temp, J_Temp, K_Temp, L_Temp, M_Temp, N_Temp, P_Temp, Q_Temp
]

# policy = {}


# Edges = ['A','B','C','D','E','H','I','L','M','N','P','Q']
# # terminals, meaning, they don't fail or go back to themseleves
# # would be excluded from self loops
# Terminals = ['A', 'Q']

# Neighbors_Directed = {
# 	'A' : [],
# 	'B' : ['A', 'C', 'F'],
# 	'C' : ['B', 'G', 'D'],
# 	'D' : ['C', 'H'],
# 	'E' : ['A', 'F', 'I'],
# 	'F' : ['E', 'B', 'G', 'J'],
# 	'G' : ['F', 'C', 'H', 'K'],
# 	'H' : ['D', 'G', 'L'],
# 	'I' : ['E', 'J', 'M'],
# 	'J' : ['I', 'F', 'K', 'N'],
# 	'K' : ['J', 'G', 'L', 'P'],
# 	'L' : ['K', 'H', 'Q'],
# 	'M' : ['I', 'N'],
# 	'N' : ['M', 'J', 'P'],
# 	'P' : ['N', 'K', 'Q'],
# 	'Q' : []
# }

# Neighbors_Undirected = {
# 	'A' : ['B', 'E'],
# 	'B' : ['A', 'C', 'F'],
# 	'C' : ['B', 'G', 'D'],
# 	'D' : ['C', 'H'],
# 	'E' : ['A', 'F', 'I'],
# 	'F' : ['E', 'B', 'G', 'J'],
# 	'G' : ['F', 'C', 'H', 'K'],
# 	'H' : ['D', 'G', 'L'],
# 	'I' : ['E', 'J', 'M'],
# 	'J' : ['I', 'F', 'K', 'N'],
# 	'K' : ['J', 'G', 'L', 'P'],
# 	'L' : ['K', 'H', 'Q'],
# 	'M' : ['I', 'N'],
# 	'N' : ['M', 'J', 'P'],
# 	'P' : ['N', 'K', 'Q'],
# 	'Q' : ['P', 'L']
# }

Rewards = {
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

# chance_nodes = ['J','G']
# decision_nodes = ['B','C','D','E','F','H','I','K','L','M','N','P']
# terminal_nodes = ['A','Q']


# for letter in edges, if letter not in terminals, then also include self loop.
# if letter not in edges, then there is no self loop possible.


# def make_random_policy():

# 	for letter in alphabet:

# 		print(letter)
# 		letters_neighbors = Neighbors_Directed[letter]

# 		# if not letters_neighbors:
# 		if letter in terminal_nodes:
# 			# we know it's a terminal node, so leave it empty
# 			policy[letter] = None

# 		elif letter in chance_nodes:
# 			policy[letter] = None

# 		else:
# 			#otherwise pick a random neighbor to assign
# 			choice = random.choice(letters_neighbors)
# 			print("initially setting policy for %s -> %s" % (letter, choice))
# 			policy[letter] = choice


def value_iteration_to_convergence(A,B,C,D,E,F,G,H,I,J,K,L,M,N,P,Q):
	# set initial loop vars
	converge = False
	x = 0

	while not converge:

		print("\nIteration %s:" % x)

		if x == 1000:
			break

		delta = 0

		A_Temp = A
		B_Temp = B
		C_Temp = C
		D_Temp = D
		E_Temp = E
		F_Temp = F
		G_Temp = G
		H_Temp = H
		I_Temp = I
		J_Temp = J
		K_Temp = K
		L_Temp = L
		M_Temp = M
		N_Temp = N
		P_Temp = P
		Q_Temp = Q

		A,B,C,D,E,F,G,H,I,J,K,L,M,N,P,Q = VI(A,B,C,D,E,F,G,H,I,J,K,L,M,N,P,Q)

		delta = max(delta,( abs(A_Temp - A) ))
		print("delta %s" % delta, end="")
		delta = max(delta,( abs(B_Temp - B) ))
		print(" delta %s" % delta, end="")
		delta = max(delta,( abs(C_Temp - C) ))
		print(" delta %s" % delta, end="")

		# 38.10093457943922
		delta = max(delta,( abs(D_Temp - D) ))
		print(" D_delta: %s" % delta, end="")

		delta = max(delta,( abs(E_Temp - E) ))
		print(" delta %s" % delta, end="")

		delta = max(delta,( abs(F_Temp - F) ))
		print(" delta %s" % delta, end="")
		delta = max(delta,( abs(G_Temp - G) ))
		print(" delta %s" % delta, end="")
		delta = max(delta,( abs(H_Temp - H) ))
		print(" delta %s" % delta, end="")
		delta = max(delta,( abs(I_Temp - I) ))
		print(" delta %s" % delta, end="")

		delta = max(delta,( abs(J_Temp - J) ))
		print(" delta %s" % delta, end="")
		delta = max(delta,( abs(K_Temp - K) ))
		print(" delta %s" % delta, end="")
		delta = max(delta,( abs(L_Temp - L) ))
		print(" delta %s" % delta, end="")
		delta = max(delta,( abs(M_Temp - M) ))
		print(" delta %s" % delta, end="")
		delta = max(delta,( abs(N_Temp - N) ))
		print(" delta %s" % delta, end="")
		delta = max(delta,( abs(P_Temp - P) ))
		print(" delta %s" % delta, end="")
		delta = max(delta,( abs(Q_Temp - Q) ))
		print(" delta %s" % delta, end="")

		print("delta %s" % delta)


		if delta < tolerance:
			print("I converge after %s iterations\n" % x)
			converge = True

		x+=1

	return A,B,C,D,E,F,G,H,I,J,K,L,M,N,P,Q



gamma = 0.85

if __name__ == '__main__':

	M = MDP()
	# set initial policy is random
	M.make_random_policy()
	M.set_initial_values()

	# for k,v in policy.items():
	# 	print("%s -> %s" % (k,v))

	# set the initial values of all states, make them be zero initially
	# set_initial_values()

	# for letter in policy.keys():

	# 	if policy[letter] is None:
	# 		pass
	# 		# we know it's terminal, just include the reward


	# make the equations
	M.set_up_probabilities()

	M.calculate_once()
	M.recalculate_policy()
	# for letter in Neighbors_Directed.keys():

	# 	# if policy[letter] is None: # or if letter in terminals
	# 	if letter in terminal_nodes:
	# 		Value = Rewards[letter]

	# 	elif letter in chance_nodes:
	# 		# split evenly among directed children
	# 		equal_chance_nodes = Neighbors_Directed[letter]
	# 		Value = Rewards[letter]

	# 		split = len(equal_chance_nodes)
	# 		for adjacent_possibility in equal_chance_nodes:
	# 			Value += ( gamma * (1/split) * adjacent_possibility)
















	# A,B,C,D,E,F,G,H,I,J,K,L,M,N,P,Q = value_iteration_to_convergence(A,B,C,D,E,F,G,H,I,J,K,L,M,N,P,Q)






















	





