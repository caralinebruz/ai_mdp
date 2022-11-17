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
from bisolver import BI



def main(discount_factor, tolerance, max_iterations, minimize_values, lines):

	# parse the file into necessary pieces
	# detect cycles (if any)
	# determine solver method (mdp vs etc....)

	p = Parser(lines)
	props = p.parse()

	m = Methodpicker(props)
	method = m.pick()

	print("method we will use: %s" % method)

	## next steps
	# implement MDP solver
	# ALSO implement backwards induction solver


	if method == "MDP":
		# use MDP solver

		M = MDP(discount_factor, tolerance, max_iterations, minimize_values, props)

		# set initial policy is random
		M.make_random_policy()
		M.set_initial_values()

		# make the equations
		M.set_up_probabilities()

		M.policy_iteration()

		for k,v in M.policy_hist.items():
			print("%s : %s" % (k,v))


		for state, final_val in M.state_values.items():
			print("%s -> %s" % (state, final_val))


	elif method == "BACKWARDS_INDUCTION":
		 pass







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

	print("discount_factor:%s, tolerance:%s" % (discount_factor, tolerance))

	main(discount_factor, tolerance, max_iterations, minimize_values, lines)


