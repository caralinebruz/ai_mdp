# AI MDP
Artificial Intelligence class lab 3

A Markov Decision Process solver using policy iteration.


## About

Given an input graph file, produces a solution. Also includes a backwards induction solver if the input graph is acyclic. Automatically determines execution method based on inputs.

## Usage

`./main.py -df .9 -tol 0.0001 [-min] data/input/maze.txt`

- `-df` is the discount factor, gamma

- `tolerance` is the desired level of convergence for mdp value iteration

- `-min` is an optional flag for minimizing values in the decision network (ie. argmin). defaults to MAX (ie.argmax).

- input graph descriptions, see pdf


## Outputs

All outputs print to STDOUT. Example of MDP policy iteration expected outs:

```
Policy for decision nodes:
  A -> Z
  B -> Z
  C -> B
  D -> C
  E -> B
  F -> E
  G -> F

Final values:
  A=0.6948712428259126
  B=0.8502906149346758
  C=0.7208162883918355
  D=0.477998721982942
  E=0.7269145451958755
  F=0.6372549990716604
  G=0.5448615867685678
  Y=-1
  Z=1
```


## Testing
This code has been tested on `cims.nyu.edu` machine: `access`.
