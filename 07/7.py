#!/usr/bin/env python3

import sys


# note: using sets instead of lists to get rid of duplicates


# get terrorists IDs
terrorist_a = input()
terrorist_b = input()

# known contacts of terrorist_a
contacts_a = set([terrorist_a])

# auxiliary graph with contacts not (yet) in the list of terrorist_a contacts
graph = {}



# adds a contact to terrorist_a known contacts
# also adds the contacts connected with him
def add(contact):
	# iterative algorithm, avoided recursive one because of stack overflow
	pending = set([contact]) # contacts to add
	while pending:
		# pops one element of set
		c = pending.pop()
		if c not in contacts_a:
			# contact not already present, add it
			contacts_a.add(c)
			# if c has also contacts, add them too
			if c in graph:
				pending.update(graph[c])
				# delete c contacts to save memory, not needed anymore
				del graph[c]



line_number = 0
# read the call log line by line
for line in open("phone_call.log"):
	
	# incremented line number here instead of at the bottom because of "continue" on the "else"
	line_number += 1
	# get contacts
	x, y = line.split()
	
	# if one of them is already in terrorist_a contacts, add the other one
	if x in contacts_a:
		add(y)
	elif y in contacts_a:
		add(x)
	else:
		# else save the connection in case x or y becomes part of terrorist_a contacts
		graph.setdefault(x, set()).add(y)
		graph.setdefault(y, set()).add(x)
		# skip next search, as no contact has been added on this line
		continue
	
	# search terrorist_b in terrorist_a contacts
	if terrorist_b in contacts_a:
		# found! now they are connected
		print("Connected at " + str(line_number-1))
		sys.exit(0)

# end reading entire log and no connection between terrorists
print("Not connected")
