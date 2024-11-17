import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

class PlatformPosition(object):
    def __init__(self):
        pass

    def start(self):
        self.platformPose = rospy.Subscriber('/my_odom_pad', Odometry, self.position)

    def position(self, data):
        x = data.pose.pose.position.x
        y = data.pose.pose.position.y
        z = data.pose.pose.position.z
        return x, y, z

def main():
    rospy.init_node('platform_position', anonymous = False)
    try:
        pp = PlatformPosition()
        rospy.spin()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
