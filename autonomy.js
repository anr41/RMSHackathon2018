var autonomy = require('ardrone-autonomy');
var mission  = autonomy.createMission();

mission.takeoff()
	       .zero()       // Sets the current state as the reference
	       .altitude(1)  // Climb to altitude = 1 meter
	       .forward(2).go({x: 0, y: 1})
	       .hover(10000)
	       .land();

	       mission.run(function (err, result) {
		           if (err) {
				console.trace("Oops, something bad happened: %s", err.message);
				mission.client().stop();
				mission.client().land();
			   } else {						                            console.log("Mission success!");
				process.exit(0);					           }
	               });
