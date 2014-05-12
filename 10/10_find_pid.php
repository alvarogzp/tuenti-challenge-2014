<?php
	# Script to find the parent PID of the server-side script so the password
	# can be calculated.
	
	# The password also depends on the current time, and the server has the
	# clock slowed a bit more than one minute, so the Date header must be
	# parsed to extract the current server minute. The hour is also needed
	# in order to calculate the server time correctly during an hour change.
	
	
	# "apt-get install php-http-request" to use this library
	require_once "HTTP/Request.php";
	
	
	# Make an initial request to get the server time
	$req =& new HTTP_Request("http://random.contest.tuenti.net/");
	$req->sendRequest();
	
	# Now try each pid from 1 to default linux pid_max (32768)
	for ($pid = 1; $pid < 32768; $pid++) {
		
		# Extract server hour and minute from last request's Date header
		# First get the Date header and split by spaces
		$date = explode(" ", $req->getResponseHeader("Date"));
		# Split the hour part
		$hour = explode(":", $date[4]);
		# The hour is the first, and the minute is the second
		$H = $hour[0];
		$i = $hour[1];
		
		# Seed the random generator with the hour, minute and pid.
		# gmmktime is used instead of mktime because the hour in Date
		# is in GMT.
		srand( gmmktime($H, $i, 0) * $pid );
		# Obtain a random number as server script does (index.php~)
		$r = rand();
		
		# Make a request with the random value as password
		# Here are some improvements, due to the high number of request
		# that will be done:
		#  - The server is specified with its IP address to avoid name
		#    resolution in each request.
		#  - Host header is manually added to reach service correctly.
		#  - User-Agent header is removed to save some bytes per request.
		$req->setURL("http://54.83.207.90/?password=" . $r);
		$req->addHeader("Host", "random.contest.tuenti.net");
		$req->removeHeader("User-Agent");
		$resp = $req->sendRequest();
		
		# Check if there is an error and print it
		if (PEAR::isError($resp)) {
			echo $resp->getMessage();
		} else {
			
			# Get the server response and compare with the error
			# message
			$response = $req->getResponseBody();
			if ($response != "wrong!") {
			
				# Password found! This means the pid is correct
				# Print the data
				echo $pid . "!\nPID=" . $pid . ", H=" . $H . ", i=" . $i . ", r=" . $r . ", Response=" . $response . "\n";
				# Exit the script
				exit;
				
			} else {
				# Incorrect pid, continue searching
				# Print actual pid to know the current state
				echo $pid . ", ";
			}
		}
	}
?>
