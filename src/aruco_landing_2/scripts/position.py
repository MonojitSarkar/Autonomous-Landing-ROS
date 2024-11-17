# !/usr/bin/python3

import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool, Empty
from geometry_msgs.msg import Twist


def listener():
    rospy.init_node('Position_get')

    rospy.Subscriber('/my_odom_pad', Odometry, position_callback)
    rospy.spin()

def position_callback(data):
    #rospy.init_node('takeoffDrone')
    #import pdb;pdb.set_trace()
    pub_posctrl = rospy.Publisher('/drone/posctrl', Bool, queue_size=1)
    pub_position = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    var_empty = Empty()
    var_bool = Bool()
    var_bool = True

    var_twist = Twist()

    var_twist.linear.x = data.pose.pose.position.x
    var_twist.linear.y = data.pose.pose.position.y
    var_twist.linear.z = data.pose.pose.position.z + 1

    pub_posctrl.publish(var_bool)
    pub_position.publish(var_twist)

    rospy.sleep(2)
    #print(data.pose.pose.position)
   

if __name__ == '__main__':
    listener()
