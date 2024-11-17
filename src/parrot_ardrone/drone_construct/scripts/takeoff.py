#!/usr/bin/env python3

import rospy
from std_msgs.msg import Bool, Empty
from geometry_msgs.msg import Twist

class DroneTakeoff():
    def __init__(self):
        rospy.init_node('takeoffDrone')
        #pub_takeoff = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
        pub_posctrl = rospy.Publisher('/drone/posctrl', Bool, queue_size=1)
        pub_position = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

        var_empty = Empty()
        var_bool = Bool()
        var_bool.data = True

        var_twist = Twist()
        for i, j, k in zip([0, 0, 3], [0,1,3], [1, 1, 3], [1, 0, 3]):
            print("Going to location: ", i,j,k)
            var_twist.linear.x = i
            var_twist.linear.y = j
            var_twist.linear.z = k 

        """var_twist.linear.x = 0
        var_twist.linear.y = 0
        var_twist.linear.z = 0"""
        

            #while not rospy.is_shutdown():
                #pub_takeoff.publish(var_empty)
        pub_posctrl.publish(var_bool)
        pub_position.publish(var_twist)

        rospy.sleep(1)

if __name__ == '__main__':
    try:
        DroneTakeoff()
    except:
        rospy.loginfo('end')
