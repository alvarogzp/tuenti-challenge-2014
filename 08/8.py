#!/usr/bin/env python


import networkx as nx # pip install networkx (https://networkx.github.io/)



# Each state is represented by a string of length 9, with each position being a
# number in the range [0, 8] representing a person.
# The graph is generated once at start with all possible combinations.
# In each table, the names are substituted by a number. Then the search is done
# using networkx graph library.



# The state with the numbers sorted, form 0 to 8, to serve as reference
SORTED_STATE = "".join([str(i) for i in range(9)])



### GRAPH GENERATION ###

# Generate a graph with all states of the table and its possible movements
def create_graph():
	g = nx.Graph()
	# Adds the nodes when it founds new in edges
	g.add_edges_from(get_all_movements())
	return g


# Yields all movements from each state to the next one, effectively returning all possible edges of the graph
def get_all_movements():
	# Using sets instead of lists to speed up:
	#  - avoiding duplicates in pending_states, and
	#  - pop(), add() and "not in" are much faster
	# States to be explored -- start with the sorted state
	pending_states = set([SORTED_STATE])
	# States already explored
	expanded = set()
	while pending_states:
		state = pending_states.pop()
		for s in get_next_states(state):
			# If already expanded, this path has already been yielded in the other direction (s -> state)
			if s not in expanded:
				# Yield the actual state and the next one as an edge of the graph
				yield state, s
				pending_states.add(s)
		expanded.add(state)


# Yields all the possible next state for a given one
def get_next_states(state):
	for i in xrange(3):
		# Cache the operation to speed up a little (this function is called too many times)
		i3 = i * 3
		for j in xrange(2):
			# Swap horizontally with the next position
			yield swap_positions(state, i3+j, i3+(j+1))
			# Swap vertically with the next down position
			yield swap_positions(state, 3*j+i, 3*(j+1)+i)


# Swaps two positions for a given state
def swap_positions(state, p1, p2):
	# Do it splitting the string and concatenating as it is faster than converting to list and joining it
	newstate = state[:p1] + state[p2] + state[p1+1:]
	newstate = newstate[:p2] + state[p1] + newstate[p2+1:]
	return newstate



### OTHER FUNCTIONS ###

# Given the tables with names, returns them with numbers from 0 to 8.
# The final table is always the SORTED_STATE, the initial one vary depending on
# the position of the names.
def translate_tables(i_table, f_table):
	# Assign each name a number from 0 to 8 corresponding to the position of
	# the name on the final table
	names = dict([ (f_table[p], str(p)) for p in range(len(f_table)) ])
	# Construct the initial table using the translation created above
	return "".join([names[n] for n in i_table]), SORTED_STATE


# Performs the search and returns the minimum number of steps needed to move from the initial table to the final one
# If they are not reachable, returns -1
def get_number_of_steps(g, i_table, f_table):
	try:
		# Use networkx to find the shortest path length
		return nx.shortest_path_length(g, i_table, f_table)
	except nx.NetworkXNoPath:
		# Path not reachable
		return -1


# Reads a table from standard input and returns it as a list of strings
def get_table():
	table = []
	for i in range(3):
		# The names are separated by a colon and a space
		table.extend(raw_input().split(", "))
	return table



### MAIN CODE ###

# First create the graph
graph = create_graph()

# Get the number of tables to reorganize
tables = int(raw_input())

for t in range(tables):
	# read empty line
	raw_input()
	# read initial table
	initial_table = get_table()
	# and the same for the final table
	raw_input()
	final_table = get_table()
	
	# Get the tables with numbers
	initial_table, final_table = translate_tables(initial_table, final_table)
	
	# Get the minimum steps
	steps = get_number_of_steps(graph, initial_table, final_table)
	
	# And print it!
	print(steps)

