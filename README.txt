---AIDEN'S ODOMETRY SIM---

SETUP:

Initialize the project by running
    FILE-PATH/qt-odometry-sim bash setup.sh
in the terminal. This script sets up the virtual environment, activates it, and installs the necessary packages.

Once you have the venv set up, you can start the program by running
    FILE-PATH/qt-odometry-sim python main.py
in the terminal.


EDITING:

If you change the C++ script make sure to run
    build.sh
which will re-compile them. Otherwise the python script will act based on the older version of the C++ script.


MANUAL:

This is a differential drive robot. It has two parallel odometers that each measure units of distance moved.
From these distances, the position and heading of the robot, relative to its starting point, can be determined.

L
|
|-----> forward
|
R


"Reset" Button: Resets the robot's position. It is helpful if the robot moves off of the screen or gets lost.

x: The robot's x position.
y: The robot's y position.
direction: The robot's heading (degrees).
size: The size of the track, or the distance between the odometers.

Checkbox "Run Wheels" / "Run Arc": Toggles the run mode (explained below)

Run Wheels: The movement of the robot is defined by the change in distance of each individual odometer.
dL: The distance recorded by the left odometer.
dR: The distance recorded by the right odometer.

Run Arc: The movement of the robot is defined by the arc angle and distance that the robot travels.
dH: The "delta heading," or the relative change in direction (degrees).
avgD: The distance traveled by the center of the robot along the arc.

Steps: The amount of steps that the robot should split the movement of dL and dR or dH and avgD into. Higher steps means a slower speed, but a higher accuracy.
Repeat: The amount of times that the robot should repeat the movement of dL and dR or dH and avgD.

"Run!" Button: Runs the operation as defined by the checkbox and the input fields.