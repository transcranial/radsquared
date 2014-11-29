//'use strict';

var os = require('os'),
    child_process = require('child_process');

var pythonXMLRPCServer_pidArray = [];
var pythonXMLRPCServer_portArray = [];
var port = 11700;
var currentServer = 0;
var allowableMemory = 512; // MB
var sizePerRPCServer = 300; // MB

exports.createRPCServers = function () {

  var numServers = Math.min(os.cpus().length, Math.floor(allowableMemory / sizePerRPCServer));
  for (var i = 0; i < numServers; i++) {
    var pythonXMLRPCServer = child_process.spawn('python', [process.env.PWD + '/nlp_engine/fetchServer.py', port]);
    pythonXMLRPCServer.stdout.on('data', function (data) {
      console.log(data.toString());
    });
    pythonXMLRPCServer.stderr.on('error', function (err) {
      console.log('Python XML-RPC server error: ' + err);
    });
    pythonXMLRPCServer.on('exit', function (code) {
      console.log('Python XML-RPC server exited with code: ' + code);
    });  
    pythonXMLRPCServer_pidArray.push(pythonXMLRPCServer.pid);
    pythonXMLRPCServer_portArray.push(port);
    // increment server port number
    port += 1;
  }

};

exports.getCurrentPort = function () {
  if (pythonXMLRPCServer_portArray.length < 1) return -1;
  var current = currentServer;
  currentServer = (currentServer + 1) % pythonXMLRPCServer_portArray.length;
  return pythonXMLRPCServer_portArray[current];
};