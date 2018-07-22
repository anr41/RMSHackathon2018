var mqtt = require('mqtt')
var client = mqtt.connect("mqtt://test.mosquitto.org")

client.on('connect', function () {
	client.subscribe('motion')
	console.log('Connected');
	client.publish('drone', 'Drone Ready')
	console.log('pushed');
})

client.on('message', function (topic, message) {
	console.log(message.toString())
		//client.end()
})
  //client.publish('drone', "Drone Ready");
  //console.log("published");
