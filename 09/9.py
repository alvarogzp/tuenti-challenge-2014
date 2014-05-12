#!/usr/bin/env python


import networkx as nx # pip install networkx


# AwesomeVille name
AWESOMEVILLE = "AwesomeVille"

# Type identifier of normal and dirt roads
TYPE_NORMAL = "normal"
TYPE_DIRT = "dirt"

# Length in meters of a car and the space between them
CAR_LENGTH = 4
CAR_SEPARATION = 1



# Given the name of the city and the list of roads to connect with AwesomeVille,
# returns the maximum numbers of cars that can go through them in an hour.
def find_number_of_cars_in_hour(city, roads):
	# Directed graph, roads are unidirectional
	g = nx.DiGraph()
	# Each road is represented by the start point, the end point and the
	# number of cars that can go through it in an hour
	for from_road, to_road, capacity in roads:
		# In case there is more than one road joining the same two points,
		# the total capacity of that section is the sum of each individual
		# road.
		# And, as the graph overwrites the old data of an edge when
		# the same one is added, capacity must be summed before adding it
		if g.has_edge(from_road, to_road):
			capacity += g[from_road][to_road]['capacity']
		# Add edge with the capacity as an attribute, used later when
		# calculating the max flow
		g.add_edge(from_road, to_road, capacity=capacity)
	# Obtain the maximum flow of the graph from the city to AwesomeCity, using
	# the capacity attribute as the capacity of the edge
	return nx.max_flow(g, city, AWESOMEVILLE)


# Return the number of cars that can go through at a given speed in km/h and with
# the given number of lanes
def cars_in_hour(speed, lanes):
	# Converts the speed to m/h, divide by the length of a car plus the separation
	# between them (it will always be an integer as speed was previously multiplied
	# by 1000 and the divisor is 5), and multiply by the number of lanes
	return ((speed * 1000) / (CAR_LENGTH + CAR_SEPARATION)) * lanes



# Get the number of cities that need to be calculated
number_of_cities = int(raw_input())

for c in xrange(number_of_cities):
	# Get the city name
	name_city = raw_input()
	# The speed is save as a dictionary, with the 'normal' and 'dirt' attributes
	# set to the corresponding value
	speed = {}
	speed[TYPE_NORMAL], speed[TYPE_DIRT] = [int(i) for i in raw_input().split()]
	# Number of intersections and roads
	number_intersections, number_roads = [int(i) for i in raw_input().split()]
	# Save the roads in a list
	roads = []
	for r in xrange(number_roads):
		# Get the four values of a road: from to type lanes
		from_road, to_road, type_road, lanes_road = raw_input().split()
		# Save the from and to values, and the calculated number of cars
		# per hour from the type of road and number of lanes
		roads.append((
			from_road,
			to_road,
			cars_in_hour(speed[type_road], int(lanes_road))
		))
	# Finally, print the name of the city and the cars that can reach AwesomeVille
	# from it each hour
	print name_city, find_number_of_cars_in_hour(name_city, roads)

