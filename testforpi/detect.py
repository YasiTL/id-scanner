# import the necessary packages
import simple_detection
from imutils.video import VideoStream
import argparse
import time
import cv2
import numpy as np
from pyzbar import pyzbar

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
# else:
#     vs = cv2.VideoCapture(args["video"])

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

    rectandbox = simple_detection.detectbarcode(frame)

    if rectandbox == None:
        rect = None
        box = None
    else:
        rect = rectandbox[0]
        box = rectandbox[1]

    # if a barcode was found, draw a bounding box on the frame
    if box is not None:
        cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)

    if box is not None:
        W = rect[1][0]
        H = rect[1][1]

        Xs = [i[0] for i in box]
        Ys = [i[1] for i in box]
        x1 = min(Xs)
        x2 = max(Xs)
        y1 = min(Ys)
        y2 = max(Ys)
        angle = rect[2]
		
        if angle < -45:
            angle += 90

        # Center of rectangle in source image
        center = ((x1+x2)/2, (y1+y2)/2)
        # Size of the upright rectangle bounding the rotated rectangle
        size = (x2-x1, y2-y1)
        M = cv2.getRotationMatrix2D(
            (size[0]/2, size[1]/2), angle, 1.0)
        # Cropped upright rectangle
        cropped = cv2.getRectSubPix(frame, size, center)
        cropped = cv2.warpAffine(cropped, M, size)
        croppedW = H if H > W else W
        croppedH = H if H < W else W
        # Final cropped & rotated rectangle
        croppedRotated = cv2.getRectSubPix(
            cropped, (int(croppedW), int(croppedH)), (size[0]/2, size[1]/2))
        print(pyzbar.decode(croppedRotated)[0])
        cv2.imshow("CroppedRotated", croppedRotated)

    # show the frame and record if the user presses a key
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# if we are not using a video file, stop the video file stream
if not args.get("video", False):
    vs.stop()

# otherwise, release the camera pointer
# else:
#     vs.release()

# close all windows
cv2.destroyAllWindows()
