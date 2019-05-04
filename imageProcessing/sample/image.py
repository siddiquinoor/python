import cv2
import glob2

img=cv2.imread("galaxy.jpg", 0)

imageFiles = glob2.glob("*.jpg")

for image in imageFiles:
    img = cv2.imread(image, 1)
    resize_image=cv2.resize(img, (100, 100))
    cv2.imwrite("resize_"+image+".jpg", resize_image)
    cv2.waitKey(500)
