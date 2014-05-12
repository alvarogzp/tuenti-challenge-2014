<?php
	# Password data is already known:
	# PID was obtained with 10_find_pid.php, and clock difference is adjusted
	# with a previous request and examination of Date header.
	
	# Server php source is in http://random.contest.tuenti.net/index.php~
	
	
	# "apt-get install php-http-request" to use this library
	require_once "HTTP/Request.php";
	
	
	# PID of server nginx (or whatever launches the php scripts),
	# found with 10_find_pid.php
	$PID = 1336;
	
	# Make an empty request to get the server time
	$req =& new HTTP_Request("http://random.contest.tuenti.net/");
	$req->sendRequest();
	
	# Extract from the Date header the hour and minutes
	$date = explode(" ", $req->getResponseHeader("Date"));
	$hour = explode(":", $date[4]);
	$H = $hour[0];
	$i = $hour[1];
	
	# Seed the random generator with the current server time and pid, as the
	# server does
	# Using gmmktime instead of mktime because the hour in Date header is in
	# GMT, not in localtime
	srand( gmmktime($H, $i, 0) * $PID );
	# Get the first random number to send as password
	$r = rand();
	
	# Get the input from stdin
	$input = trim(file_get_contents("php://stdin"));
	
	# Send the request with the input and password to the server
	$req->setURL("http://random.contest.tuenti.net/?password=" . $r . "&input=" . $input);
	$resp = $req->sendRequest();
	
	# Print the server response
	echo $req->getResponseBody();
?>
