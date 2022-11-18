# ai_mdp
A Markov Decision Process solver


## About

Given an input graph file, produces a solution. Also includes a backwards induction solver if the input graph is acyclic. Automatically determines execution method based on inputs.

## Usage

`./main.py -df .9 -tol 0.0001 [-min] data/input/maze.txt`

- `-df` is the discount factor, gamma

- `tolerance` is the desired level of convergence for mdp value iteration

- `-min` is an optional flag for minimizing values in the decision network (ie. argmin). defaults to MAX (ie.argmax).


## Testing
This code has been tested on `cims.nyu.edu` machine: `access`.
