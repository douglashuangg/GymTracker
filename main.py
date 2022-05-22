import PostureModule as pmod
import SaveModule
import cv2
import mediapipe as mp
import numpy as np
import time

def main():
    cap = cv2.VideoCapture(0)
    # ptime = 0
    # ctime = 0

    while True:
        success , img = cap.read()
        img_iso = np.empty(img.shape)
        img_iso.fill(0)
        tracker = pmod.PostureTrack()

        blur = cv2.GaussianBlur(img , (5 , 5) , cv2.BORDER_DEFAULT)
        # canny = cv2.Canny(blur , 125 , 175)

        img = tracker.trackPosture(img)
        img_iso = tracker.isolatePosture(img_iso)
        lmList = tracker.trackPoints(img)

        if len(lmList) != 0:
            tracker.calcAngle(img , 12 , 14 , 16)
            tracker.calcAngle(img_iso , 12 , 14 , 16)

# ** DISPLAY VIDEO WINDOWS
# ==============================================================

# ** FPS display
# ==============================================================
        # ctime = time.time()
        # fps = 1 / (ctime - ptime)
        # cv2.putText(img , str(int(fps)) , (0 , 0) , cv2.FONT_HERSHEY_PLAIN , 3 , (255 , 0 , 0) , 3)

# ** Pose Display, Isolated Pose Display
# ==============================================================
        cv2.imshow("Capture" , img)
        cv2.imshow("Isolate Pose" , img_iso)

        if cv2.waitKey(1) &0xFF == ord('x'):
            break

# Deallocate all associated memory objects
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()