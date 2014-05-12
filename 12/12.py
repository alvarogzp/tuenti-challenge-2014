#!/usr/bin/env python


import networkx as nx # pip install networkx



# Characters in map
START = "S"
END = "X"
WALL = "#"
SPACE = "."

# Possible directions
LEFT    = (-1,  0)
RIGHT   = ( 1,  0)
UP      = ( 0, -1)
DOWN    = ( 0,  1)
STOPPED = ( 0,  0)

# Directions that can continue for each one
NEXT_DIRECTION = {
	LEFT    : (LEFT , UP   ),
	RIGHT   : (RIGHT, DOWN ),
	UP      : (UP   , RIGHT),
	DOWN    : (DOWN , LEFT ),
	STOPPED : (LEFT , RIGHT, UP, DOWN),
}


# Represents a city: its map, the columns an lines
class City:

	def __init__(self, city_map, columns, lines):
		self.map = city_map
		self.columns = columns
		self.lines = lines



# Represents a position in the map with the actual direction
# Direction is one of LEFT, RIGHT, UP, DOWN or STOPPED
class Position:

	def __init__(self, x, y, direction):
		self.x = x
		self.y = y
		self.dir = direction
	
	# Returns a tuple with the data
	def to_tuple(self):
		return self.x, self.y, self.dir
	
	# Property to easily get the tuple using pos.tuple
	tuple = property(to_tuple)



# Creates a graph with all the possible paths in the city and return the shortest
# one from START to END
def calculate_shortest_path(city):
	# Directed graph: cannot go backwards
	g = nx.DiGraph()
	# Represents the current position and direction
	pos = Position(0, 0, None)
	
	for y in xrange(city.lines):
		pos.y = y
		for x in xrange(city.columns):
			pos.x = x
			cell = city.map[y][x]
			
			# The start point
			if cell == START:
				# The initial position is STOPPED, so we can go
				# in any direction available
				pos.dir = STOPPED
				for npos in next_positions(city, pos):
					g.add_edge(START, npos.tuple)
			
			# The end point
			elif cell == END:
				# Add a link to END from this position in each
				# direction to end the search in only one node
				for direction in NEXT_DIRECTION[STOPPED]:
					pos.dir = direction
					# If cannot reach, avoid wasting time
					if can_come_from(city, pos):
						g.add_edge(pos.tuple, END)
			
			# Normal point, not wall
			elif cell != WALL:
				# For each direction, if we can come from it
				# get the next positions and add a link to them
				for direction in NEXT_DIRECTION[STOPPED]:
					pos.dir = direction
					if can_come_from(city, pos):
						for npos in next_positions(city, pos):
							g.add_edge(pos.tuple, npos.tuple)
	
	try:
		# Get the shortest path length, decrease by one because link to
		# END node makes the path longer by one unit
		return nx.shortest_path_length(g, START, END) - 1
	except nx.NetworkXNoPath:
		# Cannot go from START to END, return ERROR
		return "ERROR"


# Return true if the car can reach the given position coming from that direction
def can_come_from(city, position):
	# Go one step in the inverse direction (substracting the deltas instead
	# of adding them) and check whether it is valid
	dx, dy = position.dir
	nx = position.x - dx
	ny = position.y - dy
	return car_allowed(city, nx, ny)


# Get the next valid positions for the given one
def next_positions(city, position):
	# Get the next valid directions for the current one and go there if it
	# is correct
	for ndir in NEXT_DIRECTION[position.dir]:
		dx, dy = ndir
		nx = position.x + dx
		ny = position.y + dy
		if car_allowed(city, nx, ny):
			yield Position(nx, ny, ndir)


# Return whether car is allowed to be in the given position (x, y)
def car_allowed(city, x, y):
	# Check bounds and that there isn't a wall
	return on_bounds(x, city.columns) and on_bounds(y, city.lines) and city.map[y][x] != WALL

# Returns true if value is positive and under limit
def on_bounds(v, limit):
	return v >= 0 and v < limit



for case in xrange(int(raw_input())):

	columns, lines = map(int, raw_input().split())
	
	city_map = []
	for c in xrange(lines):
		city_map.append(raw_input())
	
	# Case numbers start with 1
	print "Case #" + str(case+1) + ":", calculate_shortest_path(City(city_map, columns, lines))

