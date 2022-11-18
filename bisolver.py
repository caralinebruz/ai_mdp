#!/usr/bin/env python3

import methodpicker
from methodpicker import Node

from pprint import pprint


class Tree:
	''' Rebuilds the tree
		Allows for deeper recursion since we already checked
		for acyclic property

		*Returns:
			Entire tree for BI Solver to use
	'''
	def __init__(self, props):
		self.nodes_list = props['all_states']
		self.node_to_children_mappings = props['neighbors_directed']
		self.chance_nodes = props['chance_nodes']
		self.rewards = props['rewards']
		self.probabilities = props['probabilities']
		self.created_node_objects = None
		self.exact_p_mapping = {}
		self.root = None


	def _get_probability_of_node(self, name, child, children):
		''' For chance nodes, map the exact probabilities
			of reaching resp nodes, to their child node names

			*Returns:
				Probability of reaching this exact node
		'''
		p_zip = zip(children, self.probabilities[name])
		zipped_p = list(p_zip)

		# make it a dict of probability mapping to edges
		directed = {}
		for item in zipped_p:
			directed[item[0]] = item[1]

		p = directed[child]
		p_node = float(p)

		return p_node


	def _rebuild_tree_recursive(self, node, p_node, already_created_nodes_names):
		''' Recursive function to build out all of the tree nodes

			*Returns:
				The root node of the tree
		'''
		# immediately set probability of reaching node 
		#  as object property
		node.p_of_reaching_node = p_node

		# LEAF
		if not node.name in self.node_to_children_mappings.keys():
			node.value = self.rewards[node.name]
			node.p_of_reaching_node = p_node

		else:
			children = self.node_to_children_mappings[node.name]
			if children is None:
				# print("reached a leaf node")
				node.value = self.rewards[node.name]
				node.p_of_reaching_node = p_node

			else:
				for child in children:

					child_node = Node(child)
					already_created_nodes_names.append(child)
					p_node = float(1) 

					# ADD P TO THE CHILD NODE
					if node.name in self.chance_nodes:

						# child, node.name, children
						p_node = self._get_probability_of_node(node.name, child, children)

					self.created_node_objects[child] = child_node
					node.add_child(child_node)
					self._rebuild_tree_recursive(child_node, p_node, already_created_nodes_names)

		return self.root


	def _rebuild_build_tree(self):
		''' Wrapper function to create the root node of the tree
			Second, calls recursive function to create the rest of the tree

			*Returns:
				The built tree
		'''
		tree_root = self._rebuild_tree_recursive(self.root, 1, [])


	def get_root(self, m_root, created_node_objects):
		''' Repurposes the determined (and appropriate)
			root node found earlier, rebuilds the tree with 
			deeper recursion allowed for the bi solver

			*Returns:
				Root object of the new tree
		'''

		self.created_node_objects = created_node_objects
		self.root = m_root
		self._rebuild_build_tree()

		return self.root



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

		self.role = None
		self.state_values = {}
		self.policy = {}


	def getrole(self):
		'''Fills in the role based on CLI 
		'''
		if not self.minimize_values:
			self.role = "max"
		else:
			self.role = "min"


	def minimax(self, node, alpha, beta, chosen_node):
		'''	Performs minimax solver 
		'''

		# LEAF
		if not node.children:

			p_e = float(node.value) * node.p_of_reaching_node
			self.state_values[node.name] = node.value

			return p_e, node.name, node.name

		# CHANCE NODE
		if node.name in self.chance_nodes:

			# take the EV summation of my children
			ev = float(0)
			for child in node.children:
				score, node_name, temp = self.minimax(child, alpha, beta, child.name)

				ev+=score

			node.value = ev
			self.state_values[node.name] = self.rewards[node.name] + ev
			p = node.p_of_reaching_node
			value = self.state_values[node.name] * p

			return value, node.name, chosen_node

		# DECISION NODE
		if node.name in self.decision_nodes:

			# take argmin/argmax and record the decision in the policy
			if not self.minimize_values:
				the_max = float('-inf')

				for child in node.children:
					score, node_name, temp = self.minimax(child, alpha, beta, child.name)

					if score > the_max:
						the_max = score
						chosen_node = node_name		# save the name of the node for policy

				node.value = the_max
				self.state_values[node.name] = the_max
				self.policy[node.name] = chosen_node

				# print("%s(%s) chooses %s for %s" % (self.role, node.name, chosen_node, the_max))
				return the_max, node.name, chosen_node
			else:
				the_min = float('inf')

				for child in node.children:
					score, node_name, temp = self.minimax(child, alpha, beta, child.name)

					if score < the_min:
						the_min = score
						chosen_node = node_name

				node.value = the_min
				self.state_values[node.name] = the_min
				self.policy[node.name] = chosen_node

				# print("%s(%s) chooses %s for %s" % (self.role, node.name, chosen_node, the_min))
				return the_min, node.name, chosen_node


	def set_initial_values(self):
		'''Initially sets values to 0
		'''
		for state in self.all_states:

			if state in self.terminal_nodes:
				self.state_values[state] = float(self.rewards[state])
			else:
				self.state_values[state] = float(0)


	def solve(self):
		''' Solve the tree using minimax recursion
			Include specialized handling depending on node type
			ie. chance node vs terminal node etc.

			*Returns:
				The established policy and state values
		'''
		self.getrole()
		self.set_initial_values()

		# for k,v in self.created_node_objects.items():
		# 	print("%s, %s" % (k,v.p_of_reaching_node))

		value, node_name, chosen_node = self.minimax(self.root,float('-inf'),float('inf'),None)

		return self.policy, self.state_values
























