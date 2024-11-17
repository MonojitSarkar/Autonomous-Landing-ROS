#!/usr/bin/env python3

import rospy
from std_msgs.msg import Bool, Empty
from geometry_msgs.msg import Twist

class DroneLand():
    def __init__(self):
        rospy.init_node('landDrone')
        pub_velocity = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

        var_twist = Twist()

        var_twist.linear.x = 1
        var_twist.linear.y = 0
        var_twist.linear.z = 0
        var_twist.angular.x = 0.5
        var_twist.angular.y = 0
        var_twist.angular.z = 0
        

        
        while not rospy.is_shutdown():
            pub_velocity.publish(var_twist)

        rospy.sleep(1)

if __name__ == '__main__':
    try:
        DroneLand()
    except:
        rospy.loginfo('end')
