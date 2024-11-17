#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32, Float32MultiArray
from simple_pid import PID
from rospy_tutorials.msg import Floats
from rospy.numpy_msg import numpy_msg
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool, Empty

class Controller(object):
    def __init__(self):
        # I need to grab the camera translation vector
        self.trans = rospy.Subscriber('/translation', numpy_msg(Floats), self.callback)
        self.posctrl = rospy.Publisher('/drone/posctrl', Bool, queue_size=10)
        self.vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    
    def callback(self, data):
        # Get the x, y and z values from camera
        #import pdb; pdb.set_trace()
        current_x, current_y, current_z = data.data[0], data.data[1], data.data[2] 

        p, i, d = 0.0020, 0.000003, 0.0

        #Controller for z
        z_setpoint = 5
        z_range = 0.5
        z_upperpoint = z_setpoint + z_range
        z_lowerpoint = z_setpoint - z_range

        pid1 = PID(p, i, d, setpoint = z_setpoint)
        z_error = z_setpoint - current_z
        z_actuation = -z_error * p
        z_actuation = pid1(current_z)

        if current_z > z_lowerpoint and current_z < z_upperpoint:
            pass
            print("Holding the drone")
        else:
            self.parrot_adjust(0, 0, z_actuation)


    def parrot_hold(self):
        print('Holding the drone')
        var_twist = Twist()
        var_twist.linear.x = 0
        var_twist.linear.y = 0
        var_twist.linear.z = 0

        while not rospy.is_shutdown():
            self.vel.publish(var_twist)

    def parrot_adjust(self, x, y, z):
        print('Adjusting the drone')

        var_empty = Empty()
        var_bool = Bool()
        var_bool.data = False
        
        var_twist = Twist()
        var_twist.linear.x = x
        var_twist.linear.y = y
        var_twist.linear.z = z
        
        while not rospy.is_shutdown():
            self.posctrl.publish(var_bool)
            self.vel.publish(var_twist)

def main():
    rospy.init_node('precise_land', anonymous=True)
    controller = Controller()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
