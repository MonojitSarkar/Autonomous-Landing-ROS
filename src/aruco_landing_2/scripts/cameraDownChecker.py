#!/usr/bin/env python3

import numpy as np
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Empty

class Camera:
    
    def __init__(self):
        self.image_sub = rospy.Subscriber("/drone/down_camera/image_raw", Image, self.callback)
        self.cv_file = cv2.FileStorage('checkBoard.yaml', cv2.FILE_STORAGE_READ)
        self.camera_matrix = self.cv_file.getNode("camera_matrix").mat()
        self.dist_matrix = self.cv_file.getNode("dist_coeff").mat()
        self.cv_file.release()
        self.arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
        self.arucoParams = cv2.aruco.DetectorParameters_create()
        self.pub_land = rospy.Publisher('/drone/land', Empty, queue_size=1)

    def callback(self, data):
        bridge = CvBridge()

        try:
            cv_image = bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)

        image = cv_image
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        resized_image = cv2.resize(image, (320, 320))
        gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
        #ret, corners = cv2.findChessboardCorners(gray, (7,9), None)
        (corners, ids, rejected) = cv2.aruco.detectMarkers(gray, self.arucoDict, parameters = self.arucoParams, cameraMatrix=self.camera_matrix, distCoeff = self.dist_matrix)
        if len(corners) > 0:
            for i in range(0, len(ids)):
                rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, self.camera_matrix, self.dist_matrix)
                print('Rotational vectors are.....')
                print(rvec)
                print('Tranlational vector are....')
                print(tvec)
                cv2.aruco.drawDetectedMarkers(gray, corners,borderColor=(0, 165,100))
                cv2.aruco.drawAxis(gray, self.camera_matrix, self.dist_matrix, rvec, tvec, 0.01)
            #self.pub_land.publish(Empty())
        '''if ret == True:
            corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            cv2.drawChessboardCorners(gray, (7, 9), corners, ret)'''

        cv2.imshow('img',gray)

        cv2.waitKey(3)

def main():
    Camera()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    rospy.init_node('Camera_View', anonymous=False)
    main()
