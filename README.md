# pynput_teleop_twist_keyboard
---
## Description
```
Control your ROS2 robots dexterously using the this teleop package.
It allows you to use the arrow key to easily drive your robots.
It can easily be used inplace of the standard teleop_twist_keyboard pkg.
It depends on the python pynput module, hence the name of the package.

Before using the package, you must first install the pynput module using pip.
Download or clone the repo in your ROS2 workspace, build,
source and then run.
```

Install the python pynput module via command line using any of the following
commands:

```shell
$ pip3 install pynput
```
or
```shell
$ pip install pynput
```

## Launch
to run basically (speed and turn value defaults to 0.5 and 1.0 respectively):
```shell
$ ros2 run pynput_teleop_twist_keyboard pynput_teleop_twist_keyboard
```

one can also initially set a default speed and turn value:
```shell
$ ros2 run pynput_teleop_twist_keyboard pynput_teleop_twist_keyboard 0.4 0.8
```

## Usage

```
This node takes keypresses from the keyboard 
and publishes them as Twist messages.

------------------------------------------------
NONE CONTINOUS MODE (default mode)
drive around with arrow keys:

 [up/left]     [up]     [up/right]
                |
  [left] ---------------- [right]
                |
[down/left]   [down]   [down/right]

stops when no arrow key is pressed

For Holonomic mode (strafing), PRESS ALT key
(press again to return to non holonomic mode).

-------------------------------------------------
CONTINOUS DRIVE MODE (press CAPLOCK to activate
or deactivate back to non-continous mode)
drive around with arrow keys only:

              [up]  
                |
  [left] ---------------- [right]
                |
              [down]  

press s to stop robot

For Holonomic mode (strafing), PRESS ALT key
(press again to return to non holonomic mode).

-------------------------------------------------
q/z : increase/decrease only linear speed by 10%
w/x : increase/decrease only angular speed by 10%

press r to reset speed to the default or input speeds

CTRL-C to quit
```