#!/usr/bin/env python


import os.path
from Crypto.Cipher import AES # "pip install pycrypto" if not already installed



### CONSTANT DATA ###

DATA_FOLDER = "feeds" # Folder with the feed and timestamps data
FEED_FOLDER = os.path.join(DATA_FOLDER, "encrypted") # Encrypted feed folder
FEED_EXTENSION = ".feed" # Feeds file extension
LAST_TIME_FOLDER = os.path.join(DATA_FOLDER, "last_times") # last_times folder
LAST_TIME_EXTENSION = ".timestamp" # Last time extension

PASSWORD_LENGTH = 32 # 32 bytes, 256 bits (for aes-256-ecb)
BLOCK_SIZE = 16 # AES uses 128 bits blocks (16 bytes)



### PASSWORD FINAL CHARACTERS ###

# Generate once all the 3-character possible combinations and save as a list to
# later append each one to the truncated key obtained

# Every possible character for the password: [A-Za-z]
PASSWORD_CHARACTER = [ chr(c) for c in list(range(ord("A"), ord("Z") + 1)) + list(range(ord("a"), ord("z") + 1)) ]


# Generate all possible combinations of password characters for a given length
def generate_missing_password_characters(passwd, length):
	more_chars = length -1 > 0
	passwords = []
	for c in PASSWORD_CHARACTER:
		newpasswd = passwd + c
		if more_chars:
			passwords.extend(generate_missing_password_characters(newpasswd, length-1))
		else:
			passwords.append(newpasswd)
	return passwords


# Save the 3-character combinations for later use
PASSWORD_FINAL_CHARACTERS = generate_missing_password_characters("", 3)



### FIND COMPLETE PASSWORD ###

# Save the user passwords already obtained to avoid having to find them again
PASSWORDS = {}


# Given a truncated password, returns all the possible complete passwords
def possible_passwords(password):
	for c in PASSWORD_FINAL_CHARACTERS:
		yield password + c


# Given a truncated password, an encrypted data and its corresponding decrypted
# start, returns the complete password to decrypt the data
def find_complete_password(password, encrypted_feed, feed_start):
	# Decrypt only the first block to speed up
	encrypted_feed = encrypted_feed[:BLOCK_SIZE]
	feed_start = feed_start[:BLOCK_SIZE]
	
	for passwd in possible_passwords(password):
		# Mode defaults to ECB
		if AES.new(passwd).decrypt(encrypted_feed).startswith(feed_start):
			return passwd



### FEED DECRYPTION ###

# Decrypts the data with the given password
def decrypt_data(password, data):
	return AES.new(password).decrypt(data)


# Removes the padding of the data
def remove_padding(data):
	# Padding is done as described in PKCS#7 (http://tools.ietf.org/html/rfc5652#section-6.3)
	# The number of bytes padded is stored in the padding bytes
	# So, search the last byte and remove the number of bytes of its value
	last_char = data[-1]
	return data[:-ord(last_char)]


# Returns the decrypted content of the user feed
def get_user_feed(user_id, password):
	encrypted_feed = get_encrypted_feed(user_id)
	
	# If user password has not been obtained, find it now
	if user_id not in PASSWORDS:
		# Feed starts with the user_id and a space
		feed_start = user_id + " "
		password = find_complete_password(password, encrypted_feed, feed_start)
		# Save the password in case later is needed again
		PASSWORDS[user_id] = password
	
	return remove_padding(decrypt_data(PASSWORDS[user_id], encrypted_feed))



### GET FILE CONTENTS ###

# Returns the folder where the file for the given user is
def get_user_folder(user):
	# Folder schema: last two digits of user_id
	return user[-2:]

# Returns the encrypted feed of the user
def get_encrypted_feed(user):
	return open(os.path.join(FEED_FOLDER, get_user_folder(user), user + FEED_EXTENSION)).read()

# Returns the last timestamp of the user
def get_last_timestamp(user):
	return open(os.path.join(LAST_TIME_FOLDER, get_user_folder(user), user + LAST_TIME_EXTENSION)).read()



### MAIN ###

while True:
	
	try:
		line = raw_input()
	except EOFError:
		# No more input, end!
		break

	# Split the requested event number and friends
	line = line.split("; ")
	# Save and remove the events number from list
	events_to_print = int(line.pop(0))
	
	# Latest events obtained so far
	feed_events = []
	
	for friend in line:
		
		# Split the friend and password
		friend_id, truncated_password = friend.split(",")
		
		# If the events feed is already full, save the oldest timestamp
		# as anything older will not be shown
		last_event = feed_events[-1][0] if len(feed_events) >= events_to_print else None
		
		# If newest timestamp of friend is older than the oldest one in event feed,
		# skip this friend
		if last_event is None or last_event < int(get_last_timestamp(friend_id)):
		
			# Decrypt and get the event feed of the friend
			feed = get_user_feed(friend_id, truncated_password)
			
			# Split the events and iterate over the first events_to_print
			# events that can be shown
			for event, i in zip(feed.splitlines(), xrange(events_to_print)):
				# Split the event: user_id, timestamp, event_id
				user, time, event_id = event.split()
				# Time must be treated as an int in order to
				# compare properly
				time = int(time)
				# If timestamp is older than oldest one of event feed,
				# stop adding this friend events, as they will not be shown
				if last_event is not None and last_event >= time:
					break
				# Add timestamp and event_id to events feed
				feed_events.append((time, event_id))
			
			# Once end adding friend events, sort the event feed by
			# timestamp, newest to oldest
			# Timestamp sorting is done by default as tuples are
			# compared by comparing their elements, and timestamp is
			# the first one
			feed_events.sort(reverse=True)
			# Delete the oldest events exceeding the event limit
			del feed_events[events_to_print:]
	
	# Print the events as they are in feed_events
	print " ".join([ f[1] for f in feed_events ])

