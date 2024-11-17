#!/usr/bin/env python3

"""Writing the code to make the drone maintain its orientation at 0 degree yaw
And this code works perfectly fine"""

import rospy
from std_msgs.msg import Float32, Float32MultiArray
from simple_pid import PID
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool, Empty

class Controller(object):
    def __init__(self):
        self.trans = rospy.Subscriber('/rotation', numpy_msg(Floats), self.callback)
        self.posctrl = rospy.Publisher('/drone/posctrl', Bool, queue_size = 10)
        self.vel = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
        self.var_empty = Empty()
        self.var_bool = Bool()
        self.var_bool.data = False

        self.posctrl.publish(self.var_bool)

    def callback(self, data):
        print("Let's see how many times this function gets called")
        #import pdb; pdb.set_trace()
        current_roll, current_pitch, current_yaw = data.data[0], data.data[1], data.data[2]
        print(current_yaw)
        p, i, d = 1, 0.0003, 0.2

        yaw_setpoint = 0
        yaw_range = 0.005
        yaw_upperpoint = yaw_setpoint + yaw_range
        yaw_lowerpoint = yaw_setpoint - yaw_range

        pid1 = PID(p, i, d, setpoint = yaw_setpoint)
        #pid1.output_limits = (-0.5, 0.5)
        yaw_error = yaw_setpoint - current_yaw
        #yaw_actuation = -yaw_error * p
        #import pdb; pdb.set_trace()
        yaw_actuation = pid1(current_yaw)

        if current_yaw > yaw_lowerpoint and current_yaw < yaw_upperpoint:
            print("Drone's alignment is fine")
        else:
            self.parrot_adjust(yaw_actuation)

    def parrot_hold(self):
        print('Drone in Hover mode')
        
        var_twist = Twist()
        var_twist.linear.x = 0
        var_twist.linear.y = 0
        var_twist.linear.z = 0

        self.vel.publish(var_twist)

    def parrot_adjust(self, actuation):
        print("Adjusting the drone")
        print(actuation)
        
        var_twist = Twist()
        var_twist.angular.z = actuation

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
