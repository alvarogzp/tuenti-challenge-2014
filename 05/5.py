#!/usr/bin/env python3

# Rules from Game of Life: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life


import sys


# 8x8 grid
LINES = COLUMNS = 8

LIVE = "X"
DEATH = "-"



# returns the next state given the actual one
def next_state(state):
	# initializate new state with death cells
	new_state = [[DEATH for i in range(COLUMNS)] for i in range(LINES)]
	# iterate over each cell
	for y in range(LINES):
		for x in range(COLUMNS):
			# get the number of live neighbours
			neigh = get_live_neighbours(x, y, state)
			# and compute the next state cell
			if state[y][x] == LIVE:
				# if less than 2 neighbours, dies by underpopulation
				# if greater than 3, dies by overcrowding
				if neigh == 2 or neigh == 3:
					new_state[y][x] = LIVE
			else:
				if neigh == 3:
					# lives by reproduction
					new_state[y][x] = LIVE
	return new_state


# returns the number of live neighbour cells given a cell and a state
def get_live_neighbours(x, y, state):
	# cells to visit based on current cell
	DELTAS = (-1, 0, 1)
	# number of live neighbours
	neigh = 0
	# iterate over the deltas in x and y
	for dx in DELTAS:
		for dy in DELTAS:
			# this is the actual cell, skip it!
			if dx == 0 and dy == 0: continue
			# if neighbour is alive, count it
			if get(x+dx, y+dy, state) == LIVE:
				neigh += 1
	return neigh


# returns the status of a cell on a given state
def get(x, y, state):
	# if out-of-bounds, return DEATH
	if x < 0 or y < 0 or x >= COLUMNS or y >= LINES:
		return DEATH
	else:
		return state[y][x]



# initial state read from stdin and converted to a list of lists
actual_state = [[c for c in l.strip()] for l in sys.stdin.readlines()]
# past states
states = [actual_state]


while True:
	# get next state
	actual_state = next_state(actual_state)
	# compare with the previous states
	for s in range(len(states)):
		if actual_state == states[s]:
			# if equal, we have a loop
			print(s, len(states) - s)
			exit(0)
	# else, append to the states and continue
	states.append(actual_state)
