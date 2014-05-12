#!/usr/bin/env python3

try:
	while True:
		print(sum([int(i) for i in input().split()]))
except EOFError:
	pass
