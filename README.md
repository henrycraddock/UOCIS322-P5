# UOCIS322 - Project 5 #

Author: Henry Craddock

Contact: henrycraddock@gmail.com, hcraddoc@uoregon.edu

Forked from: https://github.com/alihassanijr/UOCIS322-P5.git

## Brief description

Reimplementation of the RUSA ACP controle time calculator with Flask, AJAX, and MongoDB.

The algorithm for calculating controle times is described here [https://rusa.org/pages/acp-brevet-control-times-calculator](https://rusa.org/pages/acp-brevet-control-times-calculator).

We are essentially replacing the calculator here [https://rusa.org/octime_acp.html](https://rusa.org/octime_acp.html).

## ACP controle times

That's *"controle"* with an *e*, because it's French, although "control" is also accepted. 
Controls are points where a rider must obtain proof of passage, and control[e] times are 
the minimum and maximum times by which the rider must arrive at the location.

The RUSA algorithm has been implemented in the file `acp_times.py`. The algorithm is broken into two
functions, `time_open()` and `time_close()`, both of which read information passed from the Flask app
`flask_brevets.py`. Although appearing simple, the algorithm has a few complexities that make it 
worth explaining. Firstly, the algorithm is based around set minimum and maximum speeds for different
control distances, a table of which can be found on the RUSA website. Essentially, a control distance
that falls in some range of the table will adhere to the minimum and maximum speeds in different chunks.

For example: A control point of 550 km will have its first 200 km calculated in the 0-200 km range,
its second 200 km calculated in the 200-400 km range, and its final 150 km calculated in the 
400-600 km range. It builds up opening and closing times sequentially. This is implemented through 
various distance checks and subtractions in `acp_times.py`.

Additionally, the accepted brevet distances of 200, 300, 400, 600, and 1000 km all have assigned 
closing times for the entire brevet, even if those times do not correspond exactly to what would 
be calculated using the algorithm.

Control times within the first 60 km are subject to different calculations. The closing times are 
determined by a speed of 20 km/hr plus an additional hour. The additional hour is due to the fact 
that the 0 km control of the entire brevet closes an hour after it opens, regardless.

The `Submit` and `Display` buttons present on the webpage are integrated with a MongoDB database. 
Each time the `Submit` button is pressed, the current entries in the calculator will replace any existing
values in the database. Clicking the `Display` button loads the data in the database into a new HTML page.

### Credits

Michal Young, Ram Durairajan, Steven Walton, Joe Istas.