#!/usr/bin/env python3
import sys
from enum import Enum

import pprint
from pprint import pprint


# DFS visit for detecting cycles
class Color(Enum):
	WHITE = 1
	GRAY = 2
	BLACK = 3


class Node:
	def __init__(self,name):
		self.name = name
		self.value = float(0)
		self.p_of_reaching_node = float(0)
		self.children = []
		self.parents = []

		self.color = Color.WHITE

	def add_child(self, child):
		child.parents.append(self)
		self.children.append(child)


class Methodpicker:
	''' Creates a graph/tree
		Chooses an appropriate root to build the tree
		Checks for cycles 

		*Returns:
			Solver method in {MDP,BackwardInduction}
	'''
	def __init__(self, props):
		self.method = None
		self.created_node_objects = {}
		self.nodes_list = props['all_states']
		self.node_to_children_mappings = props['neighbors_directed']
		self.chance_nodes = props['chance_nodes']
		self.rewards = props['rewards']
		self.probabilities = props['probabilities']
		self.created_node_objects = {}
		self.exact_p_mapping = {}
		self.root = None


	def create_adjacency_matrix(self):
		''' Create the adjacency matrix.
			I only do this to be able to calculate the 
			number of inbound edges for each node

			*Returns:
				adjacency matrix
		'''
		cols = self.nodes_list
		cols.sort()
		num = len(cols)
		index = {}

		i = 0
		for node_name in cols:
			index[node_name] = i
			i = i + 1

		adj = [[0 for col in range(num)] for row in range(num)]

		for from_node, to_list in self.node_to_children_mappings.items():

			index_num_row = index[from_node]
			# print("ROW -- %s: %s" % (from_node, index_num_row))

			if to_list is None:
				continue
			else:
				for to_node in to_list:
					index_num_col = index[to_node]
					adj[index_num_row][index_num_col] +=1

		return adj, index, num, cols


	def _sumColumn(self, m):
		# The sum of each column indicates num of inbound edges
		return [sum(col) for col in zip(*m)]


	def pick_a_root(self):
		''' Go through the adjacencies and picks the best root

			*Returns:
				Appropriate root choice
		'''
		adj, index, num, cols  = self.create_adjacency_matrix()

		incoming_edges = {}
		for node_name in cols:
			incoming_edges[node_name] = 0

		totals = self._sumColumn(adj)
		lowest = float('inf')
		root_index = None 
		root = None

		for x in range(num):
			if totals[x] == 0:

				# check if something else already took root position
				if root is not None:
					duplicate_root = ""
					for k,v in index.items():
						if v == x:
							duplicate_root = k
					message = ("ERROR: there are multiple roots in this graph, %s and %s. abort." % (root, duplicate_root))
					print(message)
					sys.exit(1)

				lowest = totals[x]
				root_index = x 

				for k,v in index.items():
					if v == x:
						root = k

		# print("ROOT IS :%s" % root)
		return root

	def _build_tree_inner(self, node, already_created_nodes_names):
		''' Recursive function to build out all of the tree nodes

			*Returns:
				The root node of the tree
		'''
		if not node.name in self.node_to_children_mappings.keys():
			node.value = self.rewards[node.name]
			# print("adding value to leaf: %s" % node.value)

		else:
			children = self.node_to_children_mappings[node.name]
		
			if children is None:
				node.value = self.rewards[node.name]
				# print("adding value to leaf: %s" % node.value)

			else:
				for child in children:
					if child not in already_created_nodes_names:

						child_node = Node(child)
						already_created_nodes_names.append(child)
						self.created_node_objects[child] = child_node

						node.add_child(child_node)
						self._build_tree_inner(child_node, already_created_nodes_names)

					else:
						# child node already exists, look up the node and add it as a child
						already_created_child_node = self.created_node_objects[child]
						node.add_child(already_created_child_node)

		return self.root


	def build_tree(self):
		''' Wrapper function to create the root node of the tree
			Second, calls recursive function to create the rest of the tree

			*Returns:
				The complete tree
		'''
		tree_root = self._build_tree_inner(self.root, [])


	def dfs_visit_cycle(self, node, found_cycle):
		''' i only do this dfs to check if dag has cycles...
		'''
		if found_cycle[0]:
			return

		node.color = Color.GRAY

		for child in node.children:

			if child.color == Color.GRAY:
				found_cycle[0] = True 
				print("found cycle. already visited node %s" % child.name)
				return

			if child.color == Color.WHITE:
				self.dfs_visit_cycle(child, found_cycle)

		node.color = Color.BLACK


	def check_for_cycles(self):
		''' Outer method to check for cycles in the graph

			*Returns:
				cyclic or acyclic attr
		'''
		found_cycle = [False]
		for k, node in self.created_node_objects.items():

			if node.color == Color.WHITE:
				self.dfs_visit_cycle(node, found_cycle)

			if found_cycle[0]:
				break

		return found_cycle[0]


	def pick(self):
		'''Creates a tree/graph
			Attempts to pick a node for a root
			Builds a tree and DFS to check for cycles

			*Returns: -> str
				MDP or BACKWARDS_INDUCTION
		'''
		item_to_be_root = self.pick_a_root()

		if not item_to_be_root:
			# if root returned is none, that means there were no
			# nodes without incoming edges
			self.method = "MDP"
			return self.method
			
		else:
			# but ok we will explicitly check for cycles because we were asked to.
			self.root = Node(item_to_be_root)
			self.created_node_objects[item_to_be_root] = self.root

			self.build_tree()

			if not self.check_for_cycles():
				self.method = "BACKWARDS_INDUCTION"
				return self.method

		self.method = "MDP"
		return self.method







