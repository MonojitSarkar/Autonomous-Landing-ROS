# !/usr/bin/python3

import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool, Empty
from geometry_msgs.msg import Twist

class PositionController:
    def __init__(self):
        self.trans = rospy.Subscriber('/my_odom_pad', Odometry, self.position_callback)
        self.pub_posctrl = rospy.Publisher('/drone/posctrl', Bool, queue_size=10)
        self.pub_position = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.posctrl = rospy.Publisher('/drone/posctrl', Bool, queue_size=1)
        self.var_bool = Bool()
        rospy.on_shutdown(self.on_shutdown)

    def position_callback(self, data):
        twist = Twist()

        var_empty = Empty()
        var_bool = Bool()
        var_bool.data = True

        print(data.pose.pose.position.x, data.pose.pose.position.y, data.pose.pose.position.z)


        twist.linear.x = data.pose.pose.position.x + 0.2
        twist.linear.y = data.pose.pose.position.y + 0.2
        twist.linear.z = data.pose.pose.position.z + 2

        self.pub_posctrl.publish(var_bool)
        self.pub_position.publish(twist)

    def on_shutdown(self):
        print('In clean Shutdown')
        self.var_bool.data = False
        self.posctrl.publish(self.var_bool)

        twist = Twist()
        twist.linear.x = 0
        twist.linear.y = 0
        twist.linear.z = 0
        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = 0

        self.pub_position.publish(twist)

def main():
    
    rospy.init_node('drone_position', anonymous = False)
        

    try:
        ps = PositionController()
        rospy.spin()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()
