#!/usr/bin/env python3

import numpy as np
import math
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Empty, Float64
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats

class Camera:
    
    def __init__(self):
        self.image_sub = rospy.Subscriber("/drone/down_camera/image_raw", Image, self.callback)
        self.cv_file = cv2.FileStorage('checkBoard.yaml', cv2.FILE_STORAGE_READ)
        self.camera_matrix = self.cv_file.getNode("camera_matrix").mat()
        self.dist_matrix = self.cv_file.getNode("dist_coeff").mat()
        self.cv_file.release()
        self.arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
        self.arucoParams = cv2.aruco.DetectorParameters_create()
        self.pose = rospy.Publisher('/pose', numpy_msg(Floats), queue_size=10)
        self.x_val = rospy.Publisher('/x_val', Float64, queue_size = 10)
        self.y_val = rospy.Publisher('/y_val', Float64, queue_size = 10)
        self.z_val = rospy.Publisher('/z_val', Float64, queue_size = 10) 
        self.R_flip = np.zeros((3, 3), dtype = np.float32)
        self.R_flip[0, 0] = 1.0
        self.R_flip[1, 1] = -1.0
        self.R_flip[2, 2] = -1.0


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
                print(tvec)
                cv2.aruco.drawDetectedMarkers(gray, corners,borderColor=(0, 165,100))
                cv2.aruco.drawAxis(gray, self.camera_matrix, self.dist_matrix, rvec, tvec, 0.01)

                R_ct = np.matrix(cv2.Rodrigues(rvec)[0])
                R_tc = R_ct.T

                roll_marker, pitch_marker, yaw_marker = self.rotationMatrixToEulerAngles(self.R_flip*R_tc)
                print('Angle of Yaw is: ', yaw_marker)

                c = np.array([tvec[0, 0, 0], tvec[0, 0, 1], tvec[0, 0, 2], roll_marker, pitch_marker, yaw_marker], dtype=np.float32)
                self.pose.publish(c)
                self.x_val.publish(tvec[0, 0, 0])
                self.y_val.publish(tvec[0, 0, 1])
                self.z_val.publish(tvec[0, 0, 2])

        '''if ret == True:
            corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            cv2.drawChessboardCorners(gray, (7, 9), corners, ret)'''

        cv2.imshow('img',gray)

        cv2.waitKey(3)

    def rotationMatrixToEulerAngles(self, R):
        assert(self.isRotationMatrix(R))

        sy = math.sqrt(R[0, 0]*R[0, 0] + R[1, 0]*R[1, 0])

        singular = sy < 1e-6

        if not singular:
            x = math.atan2(R[2, 1], R[2, 2])
            y = math.atan2(-R[2, 0], sy)
            z = math.atan2(R[1, 0], R[0, 0])
        else:
            x = math.atan2(-R[1, 2], R[1, 1])
            y = math.atan2(-R[2, 0], sy)
            z = 0

        return np.array([x, y, z])

    def isRotationMatrix(self, R):
        Rt = np.transpose(R)
        shouldBeIdentity = np.dot(Rt, R)
        I = np.identity(3, dtype=R.dtype)
        n = np.linalg.norm(I - shouldBeIdentity)
        return n < 1e-6

def main():
    Camera()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    rospy.init_node('down_camera_View', anonymous=False)
    main()
