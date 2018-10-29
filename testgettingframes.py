from imutils.video import VideoStream
import cv2
import time

vs = cv2.VideoCapture(0)

updateimages = True

time.sleep(2.0)

while True:
    frame = vs.read()
    frame = frame[1]

    cv2.imshow("Frame", frame)

    if updateimages:
        for i in range(0,10):
            cv2.imwrite('id_images/'+str(i)+'.png', frame, params=None)
            updateimages = False

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

vs.release()
cv2.destroyAllWindows()
