#!/usr/bin/env node

if ((process.version.split('.')[1]|0) < 10) {
	console.log('Please, upgrade your node version to 0.10+');
	process.exit();
}

var net = require('net');
var util = require('util');
var crypto = require('crypto');

// data to connect to the man-in-the-middle service
var options = {
	'port': 6969,
	'host': '54.83.207.90',
}

// wait for data on stdin
process.stdin.on('data', function (KEYPHRASE) {

	// get the keyphrase from stdin
	KEYPHRASE = KEYPHRASE.toString().trim();

	var dh, secret;
	var socket = net.connect(options);

	// wait for data on the socket
	socket.on('data', function(data) {
	
		// separate man-in-the-middle additional information from data payload
		data = data.toString().trim().split(':');
		
		// split payload in fields
		var datas = data[1].split("|");
		
		// data from SERVER to CLIENT
		if ( data[0] == "SERVER->CLIENT" ) {
		
			// send data back to client
			socket.write( data[1] + "\n" );
			
			// if data is server Diffie-Hellman public key
			if ( datas[0] == 'key' ) {
				// end Diffie-Hellman by obtaining the shared secret
				secret = dh.computeSecret(datas[1], 'hex');
			}
			
			// if data is server result
			else if ( datas[0] == 'result' ) {
				// decipher it
				var decipher = crypto.createDecipheriv('aes-256-ecb', secret, '');
				var message = decipher.update(datas[1], 'hex', 'utf8') + decipher.final('utf8');
				// print to stdout
				console.log(message);
				
				// close socket and exit program
				socket.end();
				process.exit();
			}
		}
		
		// data from CLIENT to SERVER
		else {
		
			// if data is client Diffie-Hellman key exchange
			if ( datas[0] == "key" ) {
				// compute our Diffie-Hellman values
				dh = crypto.createDiffieHellman(256);
				dh.generateKeys();
				// and send them to server instead of client ones
				socket.write(util.format('key|%s|%s\n', dh.getPrime('hex'), dh.getPublicKey('hex')));
			}
			
			// if data is client keyphrase
			else if ( datas[0] == 'keyphrase' ) {
				// cipher our keyphrase
				var cipher = crypto.createCipheriv('aes-256-ecb', secret, '');
				var keyphrase = cipher.update(KEYPHRASE, 'utf8', 'hex') + cipher.final('hex');
				// and send it instead of client one
				socket.write(util.format('keyphrase|%s\n', keyphrase));
			}
			
			// if none of the above message is received, send the response back to server
			// (for hello message)
			else {
				socket.write( data[1] + "\n" );
			}
			
		}
		
	});
	
});

