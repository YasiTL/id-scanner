import cv2

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0


def getFrames(frame, img_counter):
    while True:
        ret, frame = cam.read()

        if not ret:
            break

        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        break
