#!/usr/bin/env python3
import os
import sys
import getopt
import argparse

import parse
from parse import Parser

from pprint import pprint




def determine_solver_method(lines):

	pass



def main(discount_factor, tolerance, infile, lines):

	# parse the file into necessary pieces
	# detect cycles (if any)
	# determine solver method (mdp vs etc....)


	p = Parser(lines)
	props = p.parse_main()


	method = determine_solver_method(lines)












if __name__ == '__main__':
	# USAGE: 
	# 	./main.py -df .9 -tol 0.0001 data/input/maze.txt

	#
	# PARSE COMMAND LINE 
	#
	infile = "" # file
	discount_factor = 1	#default
	tolerance = 0.001
	lines = []

	parser = argparse.ArgumentParser(description='MDP parser')
	parser.add_argument('-df', help="discount factor")
	parser.add_argument('-tol', help="tolerance")
	parser.add_argument('input_file', type=argparse.FileType('r'))

	args = parser.parse_args()
	#print(args)

	if not args.df:
		print("You didn't input a discount factor. Using default of 1")
	else:
		discount_factor = args.df
	if not args.tol:
		print("You didn't input a tolerance. Using default of 0.001")
	else:
		tolerance = args.tol
	if args.input_file:
		lines = args.input_file.readlines()
		infile = args.input_file

	print("discount_factor:%s, tolerance:%s" % (discount_factor, tolerance))

	main(discount_factor, tolerance, infile, lines)


