#!/usr/bin/env python3
import os
import sys
import getopt
import argparse

import parse
from parse import Parser

import methodpicker
from methodpicker import Methodpicker

import mdpsolver
from mdpsolver import MDP

import bisolver
from bisolver import BI, Tree


def print_results(decision_nodes, policy, state_values):
	''' Prints computed policy and state values
	'''
	print("\nPolicy for decision nodes:")
	for state, policy in policy.items():
		if state in decision_nodes:
			print("\t%s -> %s" % (state, policy))

	print("\nFinal values:")
	for state, final_val in state_values.items():
		print("\t%s = %s" % (state, final_val))


def main(discount_factor, tolerance, max_iterations, minimize_values, lines):
	''' 1. Parse the input file 
		2. Check for any cycles in the input graph
			(this determines the solver method)
		3. Solve using appropriate method
	'''
	p = Parser(lines)
	props = p.parse()

	m = Methodpicker(props)
	method = m.pick()

	print("Using solver method: %s" % method)

	if method == "MDP":

		M = MDP(discount_factor, tolerance, max_iterations, minimize_values, props)
		policy, state_values = M.solve()

		# FINALLY
		print_results(M.decision_nodes,policy,state_values)

	elif method == "BACKWARDS_INDUCTION":

		t = Tree(props)
		root = t.get_root(m.root, m.created_node_objects)

		# solve using backward induction solver
		B = BI(max_iterations, minimize_values, root, m.created_node_objects, props)
		policy, state_values = B.solve()
	
		# FINALLY
		print_results(B.decision_nodes,policy,state_values)



if __name__ == '__main__':
	# USAGE: 
	# 	./main.py -df .9 -tol 0.0001 data/input/maze.txt

	#
	# PARSE COMMAND LINE 
	#
	infile = "" # file
	discount_factor = 1.0	#default
	tolerance = 0.01
	max_iterations = 100
	minimize_values = False
	lines = []

	parser = argparse.ArgumentParser(description='MDP parser')
	parser.add_argument('-df', help="discount factor")
	parser.add_argument('-tol', help="tolerance")
	parser.add_argument('-iter', help="max iterations")
	parser.add_argument('-min', action='store_true', help="minimize values as costs")
	parser.add_argument('input_file', type=argparse.FileType('r'))

	args = parser.parse_args()
	#print(args)

	if not args.df:
		print("You didn't input a discount factor. Using default of 1")
	else:
		discount_factor = float(args.df)
	if not args.tol:
		print("You didn't input a tolerance. Using default of 0.01")
	else:
		tolerance = float(args.tol)
	if not args.iter:
		print("You didn't input a max iteration. Using default of 100")
	else:
		max_iterations = args.iter

	if not args.min:
		print("You didnt use the -min flag. Using default of False")
	else:
		minimize_values = args.min

	if args.input_file:
		lines = args.input_file.readlines()
		infile = args.input_file


	main(discount_factor, tolerance, max_iterations, minimize_values, lines)


