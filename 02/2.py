#!/usr/bin/env python3

import sys

# four directions
RIGHT  = ( 1,  0)
LEFT   = (-1,  0)
UP     = ( 0, -1)
DOWN   = ( 0,  1)

# starts going to right
vx, vy = RIGHT

# starts on #
field  = { (0,0): '#' }

# continues on the right of the #
x, y = 1, 0

maxx = x
maxy = y
minx = x
miny = y

# given a char and a current direction, get the new direction
newdir = {
	"/": {
		DOWN : LEFT,
		LEFT : DOWN,
		UP : RIGHT,
		RIGHT : UP
	},
	
	"\\": {
		DOWN  : RIGHT,
		LEFT  : UP,
		UP    : LEFT,
		RIGHT : DOWN
	},
	
	"-": {
		DOWN  : DOWN,
		LEFT  : LEFT,
		UP    : UP,
		RIGHT : RIGHT
	}
}

# given a char and a direction, get the printed char
printedchar = {
	"/": {
		DOWN  : "/",
		LEFT  : "/",
		UP    : "/",
		RIGHT : "/"
	},
	
	"\\": {
		DOWN  : "\\",
		LEFT  : "\\",
		UP    : "\\",
		RIGHT : "\\"
	},
	
	"-": {
		DOWN  : "|",
		LEFT  : "-",
		UP    : "|",
		RIGHT : "-"
	}
}


# read a line, split by a #, and reverse the order (to start with the #)
line = ''.join(reversed(sys.stdin.readline().strip().split("#")))

# for each char in the line
for char in line:

	# compute the max and min values
	maxx=max(x, maxx)
	maxy=max(y, maxy)
	minx=min(x, minx)
	miny=min(y, miny)
	
	# print the char on the field
	field[(x, y)] = printedchar[char][(vx,vy)]
	
	# change the direction
	vx,vy = newdir[char][(vx, vy)]
	
	# updates the position
	x += vx
	y += vy

# iterate over the field
for j in range(miny, maxy+1):
	for i in range(minx, maxx+1):
		# print the chars, or blank if none
		print( field.get( (i,j), ' ' ), end="")
	
	# new line
	print()

