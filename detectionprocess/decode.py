# import the necessary packages
from pyzbar import pyzbar
import argparse
import cv2
import os

path = 'images'
for file in os.listdir(path):
    filename = os.fsdecode(file)
    if filename.endswith(".png"):
        image_file = os.path.join(path, filename)
        image = cv2.imread(image_file)
        barcodes = pyzbar.decode(image)
        
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 255), 2)
            print("[INFO] Found {} barcode: {} file: {}".format(barcodeType, barcodeData, image_file))
