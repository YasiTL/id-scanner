# import the necessary packages
from pyzbar import pyzbar
import argparse
import cv2
import os

directory = os.fsencode('id_images')

for file in os.listdir(directory):
	picture = file.decode('UTF-8')
	picture = 'id_images/' + picture

	image = cv2.imread(str(picture))
	barcodes = pyzbar.decode(image)

# # load the input image
# directory = os.fsencode('id_images')

# for file in os.listdir(directory):
# 	picture = file.decode('UTF-8')
# 	image = cv2.imread(picture)
# 	barcodes = pyzbar.decode(image)
	
# 	for barcode in barcodes:
# 		(x, y, w, h) = barcode.rect
# 		cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
# 		barcodeData = barcode.data.decode("utf-8")
# 		barcodeType = barcode.type
# 		text = "{} ({})".format(barcodeData, barcodeType)
# 		cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
# 		print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))

# # show the output image
# cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
# cv2.imshow("Image Window", image)
# cv2.waitKey(0)
