import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

class DronePosition(self): 
    def __init__(self):
        pass

    def start(self):
        self.platformPose = rospy.Subscriber('/my_odom_pad', Odometry, self.position)

    def position(self, data):
        x = data.position.x
        y = data.position.y
        z = data.position.z
        return x, y, z

def main():
    rospy.init_node('drone_position', anonymous = False)
    try:
        dp = DronePosition()
        rospy.spin()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
