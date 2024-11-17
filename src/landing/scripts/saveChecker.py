import numpy as np
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import rospy

cap = cv2.VideoCapture(0)

class Camera(object):
    def __init__(self):
        self.image_sub = rospy.Subscriber('/drone/down_camera/image_raw', Image, self.callback)
        self.i = 0
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    def callback(self, data):
        bridge = CvBridge()

        try:
            cv_image = bridge.imgmsg_to_cv2(data, desired_encoding = "bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)

        image = cv_image

        #resized_image = cv2.resize(image, (320, 320))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        """ret, corners = cv2.findChessboardCorners(gray, (7,7), None)

        if ret == True:
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
            img = cv2.drawChessboardCorners(image, (7, 7), corners2, ret)
            cv2.imshow('img' ,img)

            #cv2.imshow('frame', gray)"""

        cv2.imshow('frame', gray)

        k = cv2.waitKey(3)

        if k == 27:
            cv2.destroyAllWindows()
        elif k == ord('s'):
            name = 'images/img'+str(self.i)+'.jpg'
            cv2.imwrite(name, gray)
            self.i += 1

def main():
    Camera()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    rospy.init_node('Camera_View', anonymous=True)
    main()
