#!/usr/bin/env python3

import numpy as np
import rospy
import cv2
import math
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Empty
from rospy.numpy_msg import numpy_msg
from rospy_tutorials.msg import Floats

class Camera:
    
    def __init__(self):
        self.R_flip = np.zeros((3, 3), dtype=np.float32)
        self.R_flip[0, 0] = 1.0
        self.R_flip[1, 1] = -1.0
        self.R_flip[2, 2] = -1.0

        self.image_sub = rospy.Subscriber("/drone/down_camera/image_raw", Image, self.callback)
        self.cv_file = cv2.FileStorage('checkBoard.yaml', cv2.FILE_STORAGE_READ)
        self.camera_matrix = self.cv_file.getNode("camera_matrix").mat()
        self.dist_matrix = self.cv_file.getNode("dist_coeff").mat()
        self.cv_file.release()
        self.arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
        self.arucoParams = cv2.aruco.DetectorParameters_create()
        self.pub_land = rospy.Publisher('/drone/land', Empty, queue_size=1)
        self.rotation = rospy.Publisher('/rotation', numpy_msg(Floats), queue_size=10)

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

    def callback(self, data):
        bridge = CvBridge()

        try:
            cv_image = bridge.imgmsg_to_cv2(data, desired_encoding="bgr8")
        except CvBridgeError as e:
            rospy.logerr(e)

        image = cv_image
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        resized_image = cv2.resize(image, (480, 480))
        gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

        (corners, ids, rejected) = cv2.aruco.detectMarkers(gray, self.arucoDict, parameters = self.arucoParams, cameraMatrix=self.camera_matrix, distCoeff = self.dist_matrix)

        if len(corners) > 0:
            for i in range(0, len(ids)):
                ret = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, self.camera_matrix, self.dist_matrix)

                rvec, tvec = ret[0][0, 0, :], ret[1][0, 0, :]

                #print('Rotational vectors are.....')
                #print(rvec)

                """print('Tranlational vector are....')
                print(tvec)"""

                cv2.aruco.drawDetectedMarkers(gray, corners,borderColor=(0, 165,100))
                cv2.aruco.drawAxis(gray, self.camera_matrix, self.dist_matrix, rvec, tvec, 0.01)

                R_ct = np.matrix(cv2.Rodrigues(rvec)[0])
                R_tc = R_ct.T

                roll_marker, pitch_marker, yaw_marker = self.rotationMatrixToEulerAngles(self.R_flip*R_tc)
                print(tvec)

                str_attitude = "Marker Pose x=%2.3f y=%2.3f z=%2.3f"%(tvec[0], tvec[1], tvec[2])
                cv2.putText(gray, str_attitude, (0, 150), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 2, cv2.LINE_AA)

                ##roll_camera, pitch_camera, yaw_camera = self.rotationMatrixToEulerAngles(self.R_flip*R_tc)
                ##str_attitude = "CAMERA Attitude r=%4.0f p=%4.0f y=%4.0f"%(math.degrees(roll_camera), math.degrees(pitch_camera), math.degrees(yaw_camera))
                ##cv2.putText(gray, str_attitude, (0, 250), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2, cv2.LINE_AA)

            #self.pub_land.publish(Empty())
                #print(math.degrees(roll_marker), math.degrees(pitch_marker), math.degrees(yaw_marker))
                #print("In radians")
                #print(roll_marker, pitch_marker, yaw_marker)
                #a = np.array([math.degrees(roll_marker), math.degrees(pitch_marker), math.degrees(yaw_marker)])
                a = np.array([roll_marker, pitch_marker, yaw_marker], dtype=np.float32)
                self.rotation.publish(a)
                cv2.imshow('img',gray)

        cv2.waitKey(3)

def main():
    #import pdb; pdb.set_trace()
    Camera()

    try:
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    rospy.init_node('Camera_View', anonymous=False)
    main()
