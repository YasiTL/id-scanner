# import the necessary packages
import simple_detection
from imutils.video import VideoStream
import argparse
import time
import cv2
import RPi.GPIO as GPIO
import numpy as np

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
args = vars(ap.parse_args())

# if the video path was not supplied, grab the reference to the
# camera
if not args.get("video", False):
    vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)

# otherwise, load the video
else:
    vs = cv2.VideoCapture(args["video"])

# keep looping over the frames
while True:
    # grab the current frame and then handle if the frame is returned
    # from either the 'VideoCapture' or 'VideoStream' object,
    # respectively
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame

    # check to see if we have reached the end of the
    # video
    if frame is None:
        break

    # detect the barcode in the image
    # box = simple_detection.detect(frame)
    rect = simple_detection.detect(frame)
    # croppedframe = simple_detection.crop_minAreaRect(frame, rect)

    box = cv2.boxPoints(rect)
    box = np.int0(box)


    # if a barcode was found, draw a bounding box on the frame
    if box is not None:
        cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)


    # show the frame and record if the user presses a key
    cv2.imshow("Frame", frame)
    # cv2.imshow("crop", croppedframe)

    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# if we are not using a video file, stop the video file stream
if not args.get("video", False):
    vs.stop()

# otherwise, release the camera pointer
else:
    vs.release()

# close all windows
cv2.destroyAllWindows()
