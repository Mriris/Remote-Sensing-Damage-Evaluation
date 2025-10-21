import cv2
import numpy as np
from models.common import DetectMultiBackend, letterbox
img1 = cv2.resize(cv2.imread("1.JPG"),(1920,1080))
img2 = cv2.resize(cv2.imread("2.JPG"),(1920,1080))
img3 = cv2.resize(cv2.imread("3.png"),(1920,1080))
img4 = cv2.imread("4.png")
img4 = letterbox(img4,(1080,1920))[0]
img4 = cv2.copyMakeBorder(img4, 544, 0, 0, 0, cv2.BORDER_CONSTANT, value=[114,114,114])
img11 = np.vstack((img2,img1))
img12 = np.vstack((img4,img3))
img = np.concatenate([img11,img12],1)
cv2.imwrite("mix.jpg",img)

print()