from venv import main
import cv2
import tello
import time

def correction():
    f = cv2.FileStorage('cal.xml', cv2.FILE_STORAGE_READ)
    intrinsic = f.getNode("intrinsic").mat()
    distortion = f.getNode("distortion").mat()
    f.release()
    return intrinsic, distortion

def marker_detection(frame, intrinsic, distortion):

    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters =  cv2.aruco.DetectorParameters_create()

    markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(frame, dictionary, parameters=parameters)
    if(markerIds is None):
        return frame

    print(markerIds)
    frame = cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIds)
    rvec, tvec, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerCorners, 0.2, intrinsic, distortion)
    print(rvec)
    # frame = cv2.aruco.drawAxis(frame, intrinsic, distortion, rvec, tvec, 0.1)
    for i in range(len(markerIds)):
        frame = cv2.aruco.drawAxis(frame, intrinsic, distortion, rvec[i], tvec[i], 0.1)

    return frame


def main(intrinsic, distortion):

    cap = cv2.VideoCapture(0)
    drone = tello.Tello('', 8889)
    time.sleep(10)

    while(True):
        # frame = drone.read()
        rett, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # cv2.imshow('frame', frame)
        # print(fr)
        frame = marker_detection(frame, intrinsic, distortion)

        cv2.imshow('frame', frame)

        if cv2.waitKey(33) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break



if __name__ == "__main__":
    intrinsic, distortion =  correction()
    main(intrinsic, distortion)
