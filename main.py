#!/usr/bin/env python3


















if __name__ == '__main__':
	# USAGE: ./main.py -v 2 data/input/tiny.txt
	# mdp -df .9 -tol 0.0001 some-input.txt


	#
	# PARSE COMMAND LINE 
	#

	infile = "" # graph file
	lines = []

	parser = argparse.ArgumentParser(description='Colormap parser')
	parser.add_argument('-v', action='store_true', help="verbose flag")
	parser.add_argument('num_colors',type=int, nargs=1)
	parser.add_argument('graph_file', type=argparse.FileType('r'))

	args = parser.parse_args()
	# print(args)

	if args.v:
		v_verbose = True
	if args.num_colors:
		num_colors = int(args.num_colors[0])
	if args.graph_file:
		lines = args.graph_file.readlines()
		infile = args.graph_file


	map_coloring_via_dpll(infile, lines)

