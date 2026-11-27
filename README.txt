---AIDEN'S ODOMETRY SIM---

SETUP:

Initialize the project by running
    ~/odometry-sim % bash setup.sh
in the terminal. This script sets up the virtual environment (venv) and installs the necessary packages.
Afterwards you'll need to activate the venv by running
    ~/odometry-sim % source venv/bin/activate
in the terminal.

Once you have the venv set up, you can start the program by running
    ~/odometry-sim python main.py
in the terminal.


EDITING:

If you change the C++ scripts make sure to run
    ~/odometry-sim % build.sh
which will re-compile them. Otherwise the python script will act based on the older version of the C++ scripts.


MANUAL:

This is a differential drive robot. It has two parallel odometers that each measure units of distance moved.
From these distances, the position and heading of the robot, relative to its starting point, can be determined.

L---dL
|
|-----> forward
|
R-----dR

The blue lines protruding from the robot represent each wheel's displacement.
The red line represents the direction of the heading.

"Reset" Button: Resets the robot's position. It is helpful if the robot moves off of the screen or gets lost.

x: The robot's x position.
y: The robot's y position.
direction: The robot's heading (degrees).
size: The size of the track, or the distance between the odometers.

msDelay: The delay in ms between each step of the robot (read about steps below).

Button "Run Wheels" / "Run Arc": Toggles the run mode (explained below)

Run Wheels: The movement of the robot is defined by the change in distance of each individual odometer.
dL: The distance recorded by the left odometer.
dR: The distance recorded by the right odometer.

Run Arc: The movement of the robot is defined by the arc angle and distance that the robot travels.
dH: The "delta heading," or the relative change in direction (degrees).
avgD: The distance traveled by the center of the robot along the arc.

Steps: The amount of steps that the robot should split the movement of dL and dR or dH and avgD into.
       Higher steps means a slower speed, but a higher accuracy. Change msDelay to change the delay
       between each step.
Repeat: The amount of times that the robot should repeat the movement of dL and dR or dH and avgD.

"Run!" Button: Runs the operation as defined by the run mode and the input fields.
"Cancel" Button: Appears when running a robot movement. Press it to cancel the movement.