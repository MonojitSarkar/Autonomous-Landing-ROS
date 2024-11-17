#!/usr/bin/env python3

import rospy
from std_msgs.msg import Bool, Empty
from geometry_msgs.msg import Twist

rospy.init_node('position_node')

pub_takeoff = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
var_empty = Empty()
pub_takeoff.publish(var_empty)

var_bool = Bool()
pub_posctrl = rospy.Publisher('/drone/posctrl', Bool, queue_size=1)
var_bool.data = True
pub_posctrl.publish(var_bool)

var_twist = Twist()
pub_position = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
var_twist.linear.x = 1
var_twist.linear.y = 1
var_twist.linear.z = 2

pub_position.publish(var_twist)
