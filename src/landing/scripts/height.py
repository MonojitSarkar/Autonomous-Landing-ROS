#!/usr/bin/env python3

"""Writing the code to make the drone hover at a partiular height"""

import rospy
from std_msgs.msg import Float32, Float32MultiArray
from simple_pid import PID
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool, Empty

class Controller(object):
    def __init__(self):
        self.trans = rospy.Subscriber('/translation', numpy_msg(Floats), self.callback)
        self.posctrl = rospy.Publisher('/drone/posctrl', Bool, queue_size = 10)
        self.vel = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
        self.var_empty = Empty()
        self.var_bool = Bool()
        self.var_bool.data = False

        self.posctrl.publish(self.var_bool)

    def callback(self, data):
        print("Let's see how many times this function gets called")
        current_x, current_z = data.data[0], data.data[2]
        p, i, d = 0.1, 0.000003, 0.0

        z_setpoint = 5
        z_range = 0.2
        z_upperpoint = z_setpoint + z_range
        z_lowerpoint = z_setpoint - z_range

        pid1 = PID(p, i, d, setpoint = z_setpoint)
        z_error = z_setpoint - current_z
        z_actuation = -z_error * p
        z_actuation = pid1(current_z)

        x_setpoint = 0
        x_range = 0.000005
        x_upperpoint = x_setpoint + x_range
        x_lowerpoint = x_setpoint - x_range

        px, ix, dx = 1, 0.005, 0.4
        pid2 = PID(px, ix, dx, setpoint = x_setpoint)

        x_error = x_setpoint - current_x
        x_actuation = x_error * px
        x_actuation = pid2(current_x)

        if current_z > z_lowerpoint and current_z < z_upperpoint:
            self.parrot_hold()

            if current_x > x_lowerpoint and current_x < x_upperpoint:
                self.parrot_hold()
            else:
                self.parrot_adjust(x_actuation, command = 'x')

        else:
            self.parrot_adjust(z_actuation, command = 'z')

    def parrot_hold(self):
        print('Drone in Hover mode')
        
        var_twist = Twist()
        var_twist.linear.x = 0
        var_twist.linear.y = 0
        var_twist.linear.z = 0

        self.vel.publish(var_twist)

    def parrot_adjust(self, actuation, command):
        print("Adjusting the drone")
        print(actuation, command)
        
        var_twist = Twist()

        if command == 'x':
            var_twist.linear.x = actuation
        elif command == 'z':
            var_twist.linear.z = actuation
        elif command == 'y':
            var_twist.linear.y = actuation
        
        self.vel.publish(var_twist)

def main():
    rospy.init_node('height_check', anonymous=True)
    controller = Controller()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
