# import the necessary packages
import simple_detection
from imutils.video import VideoStream
import argparse
import time
import cv2
import numpy as np

vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

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

	if rect is not None:
		croppedimg = simple_detection.crop_minAreaRect(frame, rect)
		cv2.imshow("Cropped", croppedimg)


	# if a barcode was found, draw a bounding box on the frame
	if box is not None:
		cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)

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
else:
	vs.release()

# close all windows
cv2.destroyAllWindows()
