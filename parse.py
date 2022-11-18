#!/usr/bin/env python3
import sys
from pprint import pprint



class Parser:

	def __init__(self, raw_lines):
		self.nodes_list = []
		self.node_adjacency_mappings = {}
		self.rewards = {}
		self.probabilities = {}
		self.lines = [line.rstrip('\n') for line in raw_lines]

		self.chance_nodes = []
		self.decision_nodes = []
		self.terminal_nodes = []


	def raw_parse(self):
		''' Go through the file initially
				save names and values of things etc.
		'''
		for line in self.lines:

			# is a comment, skip immediately
			if line.startswith("#"):
				continue

			# is a directed mapping parent > child
			if ":" in line:
				data = line.split(':')

				# save node name
				node_name = data[0].strip(' ')
				if node_name not in self.nodes_list:
					self.nodes_list.append(node_name)

				# add the children of this to the node_adjacency_mappings
				children = data[1].lstrip()
				children = children.replace(' ','')
				children = children.strip('[] ').split(',')

				# true if all the strings are non-empty
				if all(children):
					self.node_adjacency_mappings[node_name] = children
					for i in children:
						if i not in self.nodes_list:
							self.nodes_list.append(i)

			# is a probability
			elif "%" in line:
				data = line.split('%')

				# save node name
				node_name = data[0].strip(' ')
				if node_name not in self.nodes_list:
					self.nodes_list.append(node_name)

				# add the probabilities
				probs = data[1].lstrip()
				probs = probs.split(' ')
				probs = list(map(float, probs))

				# true if all the strings are non-empty
				if all(probs):
					self.probabilities[node_name] = probs

			# is a reward
			elif "=" in line:
				data = line.split('=')

				# save node name
				node_name = data[0].strip(' ')
				if node_name not in self.nodes_list:
					self.nodes_list.append(node_name)

				# add reward to dict
				self.rewards[node_name] = int(data[1].strip(' '))


	def clean_raw_data(self):
		'''Go through data check valid things

		1. If a node has edges but no probability entry
		2. If a node has edges but no reward entry
		3. If a node has no edges it is terminal
		4. If a node has a single edge it always transitions there
		'''
		for state, edges in self.node_adjacency_mappings.items():

			# case 1
			if state not in self.probabilities.keys():
				self.decision_nodes.append(state)
				self.probabilities[state] = [float(1)]

			# case 2
			if state not in self.rewards.keys():
				self.rewards[state] = 0

			# case 4
			if len(edges) == 1:
				# it will always transition to that edge with p=1
				if state not in self.probabilities.keys():
					self.probabilities[state] = [float(1)]

		# case 3
		for state in self.nodes_list:
			if state not in self.node_adjacency_mappings.keys():
				# consider error
				if state in self.probabilities.keys():
					print("case 3: error - removing probability entry for terminal node:%s" % state)
					del self.probabilities[state]

					# pprint(self.probabilities)
				else:
					# mark as terminal, after it passes error check
					self.terminal_nodes.append(state)


	def enrich_data(self):
		# figure out which nodes are decision nodes
		for state, probs in self.probabilities.items():

			# decision node
			if len(probs) == 1:
				if state not in self.decision_nodes:
					self.decision_nodes.append(state)

			# chance node
			elif len(probs) > 1:
				if len(probs) == len(self.node_adjacency_mappings[state]):
					if state not in self.chance_nodes:
						self.chance_nodes.append(state)
				else:
					print("node doesnt qualify as decision node, but P doesnt match num edges")
					sys.exit(1)


	def clean_enriched_data(self):
		''' 6. probability checks
			5. remove invalid state names
		'''
		# case 6
		for state, probs in self.probabilities.items():

			# ensure chance node P sum to 1
			if state in self.chance_nodes:
				p_sum = 0
				for p in probs:
					p_sum+= p
				if p_sum != 1:
					print("case 6: die because probabilities for state %s not sum to 1" % state)
					sys.exit(1)

		# case 5
		for parent_state, edges in self.node_adjacency_mappings.items():
			# must have reward, probability, or edges

			for child_state in edges:
				valid = False
				if child_state in self.probabilities.keys():
					valid = True
				if child_state in self.rewards.keys():
					valid = True
				if child_state in self.node_adjacency_mappings.keys():
					valid = True

			if not valid:
				print("case 5: die because something that was listed as an edge doesnt meet one of three criteria")
				sys.exit(1)


	def parse(self):

		# go through the file initially and collect properties
		self.raw_parse()

		# error checking on inputs
		self.clean_raw_data()

		# go through collected properties and enrich the information
		self.enrich_data()

		# final checks on correctness of data
		self.clean_enriched_data()

		# print("FINAL props:")

		# print("chance nodes:")
		# print(self.chance_nodes)

		# print("decision nodes:")
		# print(self.decision_nodes)

		# print("terminal nodes:")
		# print(self.terminal_nodes)

		# print("names of all nodes in the graph:")
		# print(self.nodes_list)

		# print("node-adjacency-mappings:")
		# pprint(self.node_adjacency_mappings)

		# print("probabilities:")
		# pprint(self.probabilities)

		# print("rewards:")
		# pprint(self.rewards)


		props = {
				'all_states' : self.nodes_list,
				'neighbors_directed' : self.node_adjacency_mappings,
				'rewards' : self.rewards,
				'probabilities' : self.probabilities,
				'chance_nodes' : self.chance_nodes,
				'decision_nodes' : self.decision_nodes,
				'terminal_nodes' : self.terminal_nodes
		}

		return props







