#!/usr/bin/env python3

import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class Camera:
    def __init__(self):
        self.image_sub = rospy.Subscriber('/drone/down_camera/image_raw', Image, self.callback)
        self.imageCount = 0

    def callback(self, data):
        bridge = CvBridge()

        try:
            cv_image = bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)

        image = cv_image

        resized_image = cv2.resize(image, (320, 320))
        gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

        k = cv2.waitKey(3)

        if k == ord('s'):
            name = 'checkers/Image{}.png'.format(self.imageCount)
            cv2.imwrite(name, gray)
            self.imageCount += 1

        cv2.imshow("img", gray)
        #cv2.waitKey(3)

def main():
    Camera()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("Shutting Down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    rospy.init_node('Save_checker_images', anonymous = False)
    main()
