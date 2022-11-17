#!/usr/bin/env python3

from pprint import pprint

class BI:
	''' Deterministic Backwards Induction Solver
	'''

	def __init__(self, max_iterations, minimize_values, root, created_node_objects, props):
		self.max_iterations = max_iterations
		self.minimize_values = minimize_values

		self.root = root
		self.created_node_objects = created_node_objects

		self.rewards = props['rewards']
		self.probabilities = props['probabilities']
		self.decision_nodes = props['decision_nodes']
		self.chance_nodes = props['chance_nodes']
		self.terminal_nodes = props['terminal_nodes']
		self.all_states = props['all_states']
		self.node_to_children_mappings = props['neighbors_directed']

		self.role = "max"
		self.state_values = {}


	def getrole(self):
		'''Fills in the role based on CLI 
		'''
		if not self.minimize_values:
			self.role = "max"
		else:
			self.role = "min"


	def minimax(self, node, alpha, beta, chosen_node):

		print("\nat node %s" % node.name)
		print("p of reaching node %s" % node.p_of_reaching_node)

		# check if we are at a leaf
		if not node.children:

			if node.name in self.terminal_nodes:
				print("leaf is in here")

			p_e = float(node.value) * node.p_of_reaching_node
			print("EV of node:%s" % node.name)
			print("%s = %s * %s" % (p_e, node.value, node.p_of_reaching_node))

			self.rewards[node.name] = node.value

			return p_e, node.name, node.name


		# chance node need to return , what exactly?
		if node.name in self.chance_nodes:
			print("reached a chance node, need to pass up expected value and p of myself")

			print("node:%s, ev:%s, p:%s" % (node.name, node.value, node.p_of_reaching_node))

			# take the EV of my children
			ev = 0
			for child in node.children:
				score, node_name, temp = self.minimax(child, alpha, beta, child.name)

				ev+=score

			node.value = ev
			self.rewards[node.name] = self.rewards[node.name] + ev
			p = node.p_of_reaching_node

			print("Chance: node:%s, ev:%s, p:%s" % (node.name, node.value, node.p_of_reaching_node))

			value = ev * p
			print("value: %s" % value)

			return value, node.name, chosen_node



		# if the node is a decision node, take min/max and record the decision in the policy
		if node.name in self.decision_nodes:
			print("reached a decision node, must take the max of my children %s " % node.name)


			the_max = float('-inf')

			ev = 0
			for child in node.children:
				score, node_name, temp = self.minimax(child, alpha, beta, child.name)

				ev+=score

				if score > the_max:
					the_max = score
					chosen_node = node_name		# save the name of the node

				print("\tbacking up to parent (%s), new values themax= %s b= %s" % (node.name, the_max, beta))


			print("finished processing children of parent node, remaining ev:%s, the_max:%s, chosen_node:%s " % (ev, the_max, chosen_node))
			print("achieved EV of %s for node %s" % (ev,node.name))
			node.value = ev
			self.rewards[node.name] = ev

			print("%s(%s) chooses %s for %s" % (self.role, node.name, chosen_node, the_max))
			return the_max, node.name, chosen_node




	def set_initial_values(self):
		'''Initially sets values to 0
			Or, if they are a terminal state, sets to reward???
		'''
		
		for state in self.all_states:

			if state in self.terminal_nodes:
				self.state_values[state] = float(self.rewards[state])
			else:
				self.state_values[state] = float(0)





	def solve(self):
		print("starting game...")

		self.getrole()
		self.set_initial_values()


		for k,v in self.created_node_objects.items():

			print("%s, %s" % (k,v.p_of_reaching_node))

		value, node_name, chosen_node = self.minimax(self.root,float('-inf'),float('inf'),None)

		print("%s(%s) chooses %s for %s" % (self.role, self.root.name, chosen_node, value))

		pprint(self.rewards)
























