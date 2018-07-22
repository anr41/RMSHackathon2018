var arDrone = require('ar-drone');
var constants = require("ar-drone/lib/constants")
var video = require('dronestream')
var client  = arDrone.createClient();
var options = (
		1 << constants.options.DEMO |
		1 << constants.options.VISION_DETECT |
		1 << constants.options.MAGNETO |
		1 << constants.options.WIFI |
		1 << constants.options.ALTITUDE |
		1 << constants.options.ZIMMO_3000
		);
/*var express = require('express')
, app = express()
	, fs = require('fs')
	, path = require('path')
	, server = require('http').createServer(app)
	, io = require('socket.io').listen(server)
	;*/
/*
try {
	var config = require('./config');
} catch (err) {
	console.log('Missing or corrupted config file.');
	process.exit(-1);
}

var drone_ip = process.env.DEFAULT_DRONE_IP || '192.168.1.1';

var scripts = []
, styles = []
;*/

//client.disableEmergency();
client.config("control:outdoor", "FALSE");
client.config("general:navdata_options", options);
client.config("video:video_channel", 0);
client.config("detect:detect_type", 12);

client.on("navdata", function(data) {
	console.log("Flying: " + data.droneState.flying);
});

client.takeoff();

client
  .after(1000, function() {
	      this.config("control:altitude", 1);
	        })
  .after(2000, function() {
	      this.front(.1);
  	      this.left(.045);})
  .after(5000, function() {
	  this.up(.2);})
  //.after(3000, function() {
//	  this.front(.1);})
  .after(1000, function() {
	  this.stop();})
  .after(100, function() {
	  this.clockwise(1);})
  .after(10000, function() {
	  this.stop();})
  .after(1000, function() {
	  this.land();
		    });
