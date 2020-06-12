import cv2
import time
import datetime

for i in range(0, 5):
    cap = cv2.VideoCapture(i)
    is_camera = cap.isOpened()
    if is_camera:
        print(f"Input {i} is a valid camera value for VIDEO_SOURCE")
        ret, frame = cap.read() 
        if ret == True:
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = 'Width: ' + str(cap.get(3)) + ' Height:' + str(cap.get(4))
            datet = str(datetime.datetime.now())
            frame = cv2.putText(frame, text, (10, 50), font, 1,
                                (0, 255, 255), 2, cv2.LINE_AA)
            frame = cv2.putText(frame, datet, (10, 100), font, 1,
                                (0, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow('frame', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            else:
                break

        cap.release()
        time.sleep(3)
