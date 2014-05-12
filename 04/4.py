#!/usr/bin/env python3

import sys

# get all states and split source and target from other ones
states = [i.strip() for i in sys.stdin.readlines()]
source_state = states.pop(0)
target_state = states.pop(0)


# create the states graph initialized with no arcs
states_graph = dict([(s, []) for s in states])

# fill out the arcs by looking for states with 1 different nucleotide
for s1 in states:
	for s2 in states:
		different = 0
		for i, j in zip(s1, s2): # assume s1 & s2 have same length
			if i != j:
				different += 1
		if different == 1:
			# we can go from s1 to s2
			states_graph[s1] += [s2]


# find shortest path using backtracking
def find_shortest_path(graph, start, end, path=[]):
	path = path + [start]
	if start == end:
		return path
	if start not in graph:
		return None
	shortest = None
	for node in graph[start]:
		if node not in path:
			newpath = find_shortest_path(graph, node, end, path)
			if newpath:
				if not shortest or len(newpath) < len(shortest):
					shortest = newpath
	return shortest


# print shortest path
print("->".join(find_shortest_path(states_graph, source_state, target_state)))
