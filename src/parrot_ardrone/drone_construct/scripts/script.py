#! /usr/bin/env python3
import rospy
from std_msgs.msg import Empty

rospy.init_node('scriptControl')

empty = Empty()
takeoff = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
land = rospy.Publisher('/drone/land', Empty, queue_size=1)

while takeoff.get_num_connections() < 1:
    rospy.loginfo_throttle(2, "Waiting......")
    rospy.sleep(0.1)

takeoff.publish(empty)
rospy.sleep(2.0)
