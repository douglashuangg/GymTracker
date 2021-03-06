import cv2
import mediapipe as mp
import numpy as np
import math

class PostureTrack:
    ''' 
        Landmark collections for certain work-outs. Dictionaries structured with
        Keys: point where the angle is measured
        Lists: 2D list of landmarks that include the angle. Position [0] is the right side, Position [1] is the left
    '''
    pushUp_lm = {
        "waist" : [[12 , 24 , 28] , [11 , 23 , 27]] ,
        "knees" : [[24 , 26 , 28] , [23 , 25 , 27]] ,
        "elbows" : [[12 , 14 , 16] , [11 , 13 , 15]] ,
    }   # ** Planks will use the same landmarks as push ups

    benchPress_lm = {
        "wrist" : [[] , []] ,
        "ankles" : [[] , []] ,
        "back" : [] ,
        "waist" : [[] , []] ,
    }

    def __init__(self , static_mode=False , model_complexity=1 , smooth_landmarks=True , segmentation=False , smooth_segmentation=True , detectionCon=0.5 , trackingCon=0.5):
        self.static_mode = static_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.segmentation = segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_pose = mp.solutions.pose

    def trackPosture(self , img , draw=True):
        with self.mp_pose.Pose(
                self.static_mode ,
                self.model_complexity ,
                self.smooth_landmarks ,
                self.segmentation , 
                self.smooth_segmentation ,
                self.detectionCon , 
                self.trackingCon
            ) as pose:

            imgRGB = cv2.cvtColor(img , cv2.COLOR_BGR2RGB)
            self.results = pose.process(imgRGB)

            if self.results.pose_landmarks:
                if draw:
                    self.mp_drawing.draw_landmarks(
                        img ,
                        self.results.pose_landmarks ,
                        self.mp_pose.POSE_CONNECTIONS ,
                        # landmark_drawing_spec= self.mp_drawing_styles.get_default_pose_landmarks_style()
                    )
        return img
    
    def isolatePosture (self , img , draw= True):
        if self.results.pose_landmarks:
            if draw:
                self.mp_drawing.draw_landmarks(
                    img ,
                    self.results.pose_landmarks ,
                    self.mp_pose.POSE_CONNECTIONS ,
                    # landmark_drawing_spec= self.mp_drawing_styles.get_default_pose_landmarks_style()
                )
        
        return img
    
    def trackPoints(self , img , draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id , lm in enumerate(self.results.pose_landmarks.landmark):
                h , w , c = img.shape
                x_pos , y_pos = int(lm.x * w) , int(lm.y * h)
                self.lmList.append([id , x_pos , y_pos])
            
                if draw:
                    cv2.circle(img , (x_pos , y_pos) , 5 , (255 , 0 , 0) , cv2.FILLED)

        return self.lmList
    
    def calcAngle (self , img , p1 , p2 , p3 , draw=True):
        _ , x1 , y1 = self.lmList[p1]
        _ , x2 , y2 = self.lmList[p2]
        _ , x3 , y3 = self.lmList[p3]

        dist_1_2 = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        dist_2_3 = math.sqrt((x3 - x2)**2 + (y3 - y2)**2)
        dist_1_3 = math.sqrt((x3 - x1)**2 + (y3 - y1)**2)
        angle = math.degrees(math.acos((dist_1_2**2 + dist_2_3**2 - dist_1_3**2) / (2 * dist_1_2 * dist_2_3)))

        if draw:
            cv2.line(img , (x1 , y1) , (x2 , y2) , (255 , 255 , 255) , 2)
            cv2.circle(img , (x1 , y1) , 10 , (0 , 0 , 255) , cv2.FILLED)
            cv2.circle(img , (x1 , y1) , 15 , (0 , 0 , 255) , 2)

            cv2.line(img , (x2 , y2) , (x3 , y3) , (255 , 255 ,255) , 2)
            cv2.circle(img , (x2 , y2) , 10 , (0 , 0 , 255) , cv2.FILLED)
            cv2.circle(img , (x2 , y2) , 15 , (0 , 0 , 255) , 2)

            cv2.circle(img , (x3 , y3) , 10 , (0 , 0 , 255) , cv2.FILLED)
            cv2.circle(img , (x3 , y3) , 15 , (0 , 0 , 255) , 2)

            cv2.putText(img , str(int(angle)) , (x2 + 20 , y2 + 10) , cv2.FONT_HERSHEY_PLAIN , 1 , (255 , 255 , 255))

# ** use main() to test any new functions to PostureTrack class or PostureModule.py
def main():
    cap = cv2.VideoCapture(0)

    while True:
        success , img = cap.read()
        img_iso = np.empty(img.shape)
        img_iso.fill(0)
        tracker = PostureTrack()

        blur = cv2.GaussianBlur(img , (5 , 5) , cv2.BORDER_DEFAULT)
        canny = cv2.Canny(blur , 125 , 175)

        img = tracker.trackPosture(img)
        img_iso = tracker.isolatePosture(img_iso)
        lmList = tracker.trackPoints(img)

        if len(lmList) != 0:
            tracker.calcAngle(img , 12 , 14 , 16)
            tracker.calcAngle(img_iso , 12 , 14 , 16)

# DISPLAY VIDEO WINDOWS
# ==============================================================
# FPS display
        # ctime = time.time()
        # fps = 1 / (ctime - ptime)
        # cv2.putText(img , str(int(fps)) , (0 , 0) , cv2.FONT_HERSHEY_PLAIN , 3 , (255 , 0 , 0) , 3)

# ==============================================================
# Pose Display, Isolated Pose Display
        cv2.imshow("Capture" , img)
        cv2.imshow("Isolate Pose" , img_iso)

        if cv2.waitKey(1) &0xFF == ord('x'):
            break

# Deallocate all associated memory objects
    cv2.destroyAllWindows()

# if __name__ == '__main__':
#     main()