#!/usr/bin/env python3
import os
import sys
import getopt
import argparse

import parse
















if __name__ == '__main__':
	# USAGE: ./main.py -v 2 data/input/tiny.txt
	# mdp -df .9 -tol 0.0001 some-input.txt

	# ./main.py -df .9 -tol 0.0001 data/input/maze.txt


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


