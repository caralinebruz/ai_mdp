#!/usr/bin/env python3

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
		self.node_to_children_mappings = props['neighbors_directed']

		self.role = "max"


	def getrole(self):
		'''Fills in the role based on CLI 
		'''
		if not self.minimize_values:
			self.role = "max"
		else:
			self.role = "min"


	def minimax(self, node, role, alpha, beta, chosen_node):

		# check if we are at a leaf
		if not node.children:

			if node.name in self.terminal_nodes:
				print("leaf is in here")
			else:
				print("someething is up.")

			return float(node.value), node.name, chosen_node

		curr_role = self.role 
		next_role = self.role

		if self.role == "max":
			alpha = float('-inf')

			for child in node.children:
				score, node_name, temp = self.minimax(child, next_role, alpha, beta, child.name)

				if score > alpha:
					alpha = score
					chosen_node = node_name		# save the name of the node

				print("\tbacking up to parent (%s), new values a= %s b= %s" % (node.name, alpha, beta))

				# if ab_prune:
				# 	if alpha >= beta:
				# 		print("\t%s pruning node:%s bc alpha %s >= beta %s" % (role, node.name, alpha, beta))
				# 		node.prune = True
				# 		break

			print("%s(%s) chooses %s for %s" % (self.role, node.name, chosen_node, alpha))
			return alpha, node.name, chosen_node

		if self.role == "min":
			beta = float('inf')

			for child in node.children:
				score, node_name, temp = minimax(child, next_role, alpha, beta, child.name)

				if score < beta:
					beta = score
					chosen_node = node_name		# save the name of the node

				print("\tbacking up to parent (%s), new values a= %s b= %s" % (node.name, alpha, beta))

				# if ab_prune:
				# 	if alpha >= beta:
				# 		print("\t%s pruning node:%s bc alpha %s >= beta %s" % (role, node.name, alpha, beta))
				# 		node.prune = True
				# 		break

			print("%s(%s) chooses %s for %s" % (self.role, node.name, chosen_node, beta))
			return beta, node.name, chosen_node





	def solve(self):
		print("starting game...")

		self.getrole()

		value, node_name, chosen_node = self.minimax(self.root,self.role,float('-inf'),float('inf'),None)

		print("%s(%s) chooses %s for %s" % (self.role, self.root.name, chosen_node, value))






















