#!/usr/bin/env python3

import sys
import math

# read the number of cases
N = int( sys.stdin.readline() )

# for each case
for i in range(N):

	# read x,y
	x,y = sys.stdin.readline().split()
	
	# as integers
	x = int(x)
	y = int(y)
	
	# pitagoras algorithm to get the hypotenuse, with two decs
	result = round( math.sqrt( x*x + y*y ), 2 )
	
	# if result has no decs
	if result == int(result):
		# print the integer part
		print( int(result) )
	else:
		# if it has decs, print the full number
		print( result )

