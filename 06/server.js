#!/usr/bin/env node

// Modified server.js to print keyphrase received
// Not needed to solve challenge, but can be used to know what keyphrase is sending the real client

if ((process.version.split('.')[1]|0) < 10) {
	console.log('Please, upgrade your node version to 0.10+');
	process.exit();
}

var net = require('net');
var util = require('util');
var crypto = require('crypto');
var fs = require('fs');

net.createServer(function(socket) {

	var dh, secret, state = 0;

	socket.on('data', function(data) {

		data = data.toString().trim().split('|');

		if (state == 0 && data[0] == 'hello?') {
			socket.write('hello!\n');
			state++;
		} else if (state == 1 && data[0] == 'key') {
			dh = crypto.createDiffieHellman(data[1], 'hex');
			dh.generateKeys();
			secret = dh.computeSecret(data[2], 'hex');
			socket.write(util.format('key|%s\n', dh.getPublicKey('hex')));
			state++;
		} else if (state == 2 && data[0] == 'keyphrase') {
			var decipher = crypto.createDecipheriv('aes-256-ecb', secret, '');
			var keyphrase = decipher.update(data[1], 'hex', 'utf8') + decipher.final('utf8');
			console.log(keyphrase);
			socket.end();
		} else {
			socket.write('Error\n');
			socket.end();
		}
	});

}).listen(6767, '0.0.0.0', function() {
	console.log('listening...');
});
