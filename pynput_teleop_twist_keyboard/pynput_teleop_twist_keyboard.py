from email.policy import default
import sys

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist

from pynput.keyboard import Key, Listener







arg_msg = """
enter velocity args in format <linear vel> <angular vel>
        """

def process_args_vel():
    speed = 0.5
    turn = 1.0
    try:
        if len(sys.argv) == 1:
            print(arg_msg)
            print("using default values")
            return speed, turn
        else:
            print("using entered velocity values")
            speed = float(sys.argv[1])
            turn = float(sys.argv[2])
            return speed, turn
    except Exception as e:
        print(e)
        print(arg_msg)
        print("using default values")
        return speed, turn




msg = """
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

For Holonomic mode (strafing), 
hold down the shift key.

-------------------------------------------------
CONTINOUS DRIVE MODE (press caplock to activate
or deactivate back to non-continous mode)
drive around with arrow keys only:

              [up]  
                |
  [left] ---------------- [right]
                |
              [down]  

press key s to stop robot

For Holonomic mode (strafing), 
hold down the shift key.

-------------------------------------------------
q/z : increase/decrease only linear speed by 10%
w/x : increase/decrease only angular speed by 10%

ALT to reset speed

CTRL-C to quit
"""



class Teleop(Node):
    def __init__(self):
        super().__init__(node_name="pynput_teleop_twist_keyboard_node") # initialize the node name


        self.speedBindings = {
            # 'q': (1.1, 1.1),
            # 'z': (.9, .9),
            'q': (1.1, 1),
            'z': (.9, 1),
            'w': (1, 1.1),
            'x': (1, .9),
        }
        self.speed_ctrl_keys = ['q', 'z', 'w', 'x']

        self.default_speed, self.default_turn = process_args_vel()

        self.speed = self.default_speed
        self.turn = self.default_turn
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.th = 0.0

        self.holonomic_mode = False
        self.continuos_mode = False
        self.can_print = True

        self.status = 0

        self.Mode = ["non_holonomic","non_continous"]


        self.send_cmd = self.create_publisher(Twist, 'cmd_vel', 10)

        # # the timer will automatically run the timer callback function
        # # for every timer_period
        timer_period = 0.05
        self.timer = self.create_timer(timer_period, self.publish_twist)

        # ...or, in a non-blocking fashion:
        listener = Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()
        # listener.join()

        print(msg)
        print("mode: ", self.Mode)
            


    def publish_twist(self):
        self.twist = Twist()
        
        self.twist.linear.x = self.x * self.speed
        self.twist.linear.y = self.y * self.speed
        self.twist.linear.z = 0.0
        self.twist.angular.x = 0.0
        self.twist.angular.y = 0.0
        self.twist.angular.z = self.th * self.turn
        self.send_cmd.publish(self.twist)

        self.print_speed()

    def print_speed(self):
        if self.can_print:
            if (self.status == 14):
                print(msg)
                print("mode: ", self.Mode)
            self.status = (self.status + 1) % 15

            print('currently:\tspeed=%s\tturn=%s' % (self.speed, self.turn))
            self.can_print=False


    def reset_speed(self):
        self.speed = self.default_speed
        self.turn = self.default_turn
        self.can_print=True

    def on_press(self, key):       
        if key == Key.up:
            if self.continuos_mode:
                self.x = 1
                self.th = 0
                self.y = 0
            else:
                if self.x == 0:
                    self.x = 1
                
        elif key == Key.down:
            if self.continuos_mode:
                self.x = -1
                self.th = 0
                self.y = 0
            else:
                if self.x == 0:
                    self.x = -1



        if key == Key.left:
            if self.continuos_mode:
                if not self.holonomic_mode:
                    self.th = 1
                else:
                    self.y = 1
                self.x = 0
            else:
                if not self.holonomic_mode:
                    if self.th == 0:
                        self.th = 1
                else:
                    if self.y == 0:
                        self.y = 1
                
        elif key == Key.right:
            if self.continuos_mode:
                if not self.holonomic_mode:
                    self.th = -1
                else:
                    self.y = -1
                self.x = 0
            else:
                if not self.holonomic_mode:
                    if self.th == 0:
                        self.th = -1
                else:
                    if self.y == 0:
                        self.y = -1



        if key == Key.shift:
            if self.holonomic_mode==True:
                self.holonomic_mode=False
                self.Mode[0] = "non_holonomic"
            else:
                self.holonomic_mode=True
                self.Mode[0] = "holonomic"
                self.th = 0
            
            print("mode: ", self.Mode)
            
        
        if key == Key.caps_lock:
            if self.continuos_mode==True:
                self.continuos_mode = False
                self.Mode[1] = "non_continuous"
                self.x = 0.0
                self.y = 0.0
                self.z = 0.0
                self.th = 0.0
            else:
                self.continuos_mode = True
                self.Mode[1] = "continuous"
                self.x = 0.0
                self.y = 0.0
                self.z = 0.0
                self.th = 0.0
            
            print("mode: ", self.Mode)


        if key == Key.alt:
            self.reset_speed() 

        
        if hasattr(key, 'char'):
            if key.char in self.speed_ctrl_keys:
                self.speed = self.speed * self.speedBindings[key.char][0]
                self.turn = self.turn * self.speedBindings[key.char][1]
                self.can_print=True

            elif key.char == 's':
                self.x = 0.0
                self.y = 0.0
                self.z = 0.0
                self.th = 0.0

                    
    def on_release(self, key):

        if key == Key.up:
            if self.continuos_mode:
                pass
            else:
                if self.x == 1:
                    self.x = 0
                
        elif key == Key.down:
            if self.continuos_mode:
                pass
            else:
                if self.x == -1:
                    self.x = 0



        if key == Key.left:
            if self.continuos_mode:
                pass
            else:
                if not self.holonomic_mode:
                    if self.th == 1:
                        self.th = 0
                else:
                    if self.y == 1:
                        self.y = 0
     
        elif key == Key.right:
            if self.continuos_mode:
                pass
            else:
                if not self.holonomic_mode:
                    if self.th == -1:
                        self.th = 0
                else:
                    if self.y == -1:
                        self.y = 0

        if key == Key.esc:
            # Stop listener
            return False
        






def main(args=None):
    # Initialize the rclpy library
    rclpy.init(args=args)

    # Create the publisher node
    teleop = Teleop()

    # spin the node so the call back function is called
    rclpy.spin(teleop)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    teleop.destroy_node()

    # Shutdown the ROS client library for Python
    rclpy.shutdown() 



if __name__=='__main__':
    main()