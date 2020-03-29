import cv2

img = cv2.imread('ear/test5.png')
cv2.GaussianBlur(img,(3,3),1)
edges = cv2.Canny(img,5,30)
cv2.namedWindow('IMG')
cv2.imshow('IMG',edges)
cv2.waitKey()