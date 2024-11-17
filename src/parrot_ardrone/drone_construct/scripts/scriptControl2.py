#! /usr/bin/env python3

import rospy
from std_msgs.msg import Empty

class DroneTakeoffLand(object):
    def __init__(self):
        rospy.init_node("/start")
        self.pub_takeoff = rospy.Publisher('/drone/takeoff', Empty, queue_size=1)
        self.pub_land = rospy.Publisher('/drone/land', Empty, queue_size=1)

        self.empty = Empty()

        """while pub_takeoff.get_num_connections() < 1:
            rospy.loginfo_throttle(2, "Waiting.....")
            ropsy.sleep(0.1)
        pub_takeoff.publish(empty)
        ropsy.sleep(2.0)
        print('works')
        land.publish(empty)"""



if __name__ == '__main__':
    try:
        print('start')
        import pdb; pdb.set_trace()
        dd = DroneTakeoffLand()
        while pub_takeoff.get_num_connections() < 1:
            rospy.loginfo_throttle(2, "Waiting....")
            rospy.sleep(0.1)
        dd.pub_takeoff.publish(dd.empty)
        rospy.sleep(2.0)
        print('Works')
        dd.pub_land.publish(dd.empty)
    except:
        rospy.loginfo('end')
