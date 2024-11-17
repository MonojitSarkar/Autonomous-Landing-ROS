#!/usr/bin/env python3 

""" Code to test how /cmd/vel works in Parrot Drone"""

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool, Empty


class Controller(object):
    def __init__(self):
        self.vel = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.posctrl = rospy.Publisher('/drone/posctrl', Bool, queue_size=1)
        self.var_bool = Bool()
        self.var_bool.data = False
        self.posctrl.publish(self.var_bool)
        

    def parrot_hold(self):
        twist = Twist()
        twist.linear.x = 0
        twist.linear.y = 0
        twist.linear.z = 0

        while not rospy.is_shutdown():
            self.vel.publish(twist)

    def parrot_adjust(self, x, y, z, roll, pitch, yaw):
        twist = Twist()
        twist.linear.x = x
        twist.linear.y = y
        twist.linear.z = z
        twist.angular.x = roll
        twist.angular.y = pitch
        twist.angular.z = yaw

        while not rospy.is_shutdown():
            self.vel.publish(twist)

def main():
    rospy.init_node('test', anonymous = True)
    controller = Controller()
    controller.parrot_adjust(0, 0.5, 0, 0, 0, 0)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
