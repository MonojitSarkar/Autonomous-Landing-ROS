import cv2
import numpy as np
import glob

cbrow, cbcol = 7, 9
images = glob.glob('*.png')
count = 0
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((cbrow*cbcol, 3), np.float32)
objp[:, :2] = np.mgrid[0:cbcol, 0:cbrow].T.reshape(-1, 2)

objpoints, imgpoints = [], []

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, (7,9), None)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)
        cv2.drawChessboardCorners(gray, (7, 9), corners2, ret)
        count += 1

    #cv2.imshow('image', gray)
    print('[INFO] READING.....'+fname)
    #cv2.waitKey(0)

cv2.destroyAllWindows()
print(count)

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

cv_file = cv2.FileStorage("checkBoard.yaml", cv2.FILE_STORAGE_WRITE)
cv_file.write('camera_matrix', mtx)
cv_file.write('dist_matrix', dist)
cv_file.release()
