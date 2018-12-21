# import the necessary packages
import numpy as np
import cv2
import imutils

# def crop_minAreaRect(img, rect):

#     # rotate img
#     angle = rect[2]
#     rows,cols = img.shape[0], img.shape[1]
#     M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
#     img_rot = cv2.warpAffine(img,M,(cols,rows))

#     # rotate bounding box
#     rect0 = (rect[0], rect[1], 0.0) 
#     box = cv2.boxPoints(rect0)
#     pts = np.int0(cv2.transform(np.array([box]), M))[0]    
#     pts[pts < 0] = 0

#     # crop
#     img_crop = img_rot[pts[1][1]:pts[0][1], 
#                        pts[1][0]:pts[2][0]]

#     return img_crop

def detect(image):
	# convert the image to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# compute the Scharr gradient magnitude representation of the images
	# in both the x and y direction using OpenCV 2.4
	ddepth = cv2.CV_32F
	gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
	gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)

	# subtract the y-gradient from the x-gradient
	gradient = cv2.subtract(gradX, gradY)
	gradient = cv2.convertScaleAbs(gradient)

	# blur and threshold the image
	blurred = cv2.blur(gradient, (9, 9))
	(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)

	# construct a closing kernel and apply it to the thresholded image
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
	closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

	# perform a series of erosions and dilations
	closed = cv2.erode(closed, None, iterations=4)
	closed = cv2.dilate(closed, None, iterations=4)

	# find the contours in the thresholded image
	cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]

	# if no contours were found, return None
	if len(cnts) == 0:
		return None

	# otherwise, sort the contours by area and compute the rotated
	# bounding box of the largest contour
	c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
	rect = cv2.minAreaRect(c)
	box = cv2.boxPoints(rect)
	box = np.int0(box)

	# return the bounding box of the barcode
	return box
	# return rect
