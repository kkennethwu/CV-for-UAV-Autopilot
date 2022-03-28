import tello
from tello_control_ui import TelloUI
import numpy as np
import cv2
import time
import keyboard

def main():
    drone = tello.Tello('', 8889)
    time.sleep(20)
    objpoints=[]
    imgpoints=[]
    imgnum=0
    objp=np.zeros((6*9, 3), np.float32)
    objp[:, :2]=np.mgrid[0:9, 0:6].T.reshape(-1, 2)


    while(imgnum<4):
        frame = drone.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        ret, corner = cv2.findChessboardCorners(gray, (9,6),None)

        #print(ret)
        if keyboard.is_pressed("r"):
            if ret==True:
                cv2.cornerSubPix(gray, corner, (11,11), (-1,-1), (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1))
                objpoints.append(objp)
                imgpoints.append(corner)
                imgnum=imgnum+1
                cv2.waitKey(33)

        cv2.imshow('frame',frame)
        cv2.waitKey(33)

    ret, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, (480,640), None, None)
    print(cameraMatrix)
    print(distCoeffs)
    f = cv2.FileStorage('cal.xml', cv2.FILE_STORAGE_WRITE)
    f.write("intrinsic",cameraMatrix)
    f.write("distortion", distCoeffs)
    f.release()

if __name__ == '__main__':
    main()