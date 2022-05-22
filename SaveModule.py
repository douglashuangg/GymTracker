import cv2
import mediapipe as mp
import os

def saveVideo(videoCapture , fileName):
    vid_path = os.path.abspath(f"C:/GymTracker/videos/{fileName}")
    vid_cod = cv2.VideoWriter_fourcc('X' , 'V' , 'I' , 'D')
    output = cv2.VideoWriter(vid_path, vid_cod, 20.0, (640,480))

    while(True):
        # Capture each frame of webcam video
        ret,frame = videoCapture.read()
        cv2.imshow("My cam video", frame)
        output.write(frame)
        # Close and break the loop after pressing "x" key
        if cv2.waitKey(1) &0XFF == ord('x'):
            break
    # close the already opened camera
    videoCapture.release()
    # close the already opened file
    output.release()
    pass

# ** Use main() to test any new functions in SaveModule.py
def main():
    vid_capture = cv2.VideoCapture(0)
    saveVideo(vid_capture , "video_capture_1.avi")
    
    # close the window and de-allocate any associated memory usage
    cv2.destroyAllWindows()

# if __name__ == '__main__':
#     main()