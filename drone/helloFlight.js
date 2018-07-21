var arDrone = require('ar-drone');
var client = arDrone.createClient();
client.takeoff();
    setTimeout(function () {
     client.land();
    }, 15000); 

