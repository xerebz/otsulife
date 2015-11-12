import numpy as np
import cv2
from matplotlib import pyplot as plt

img1 = cv2.imread('044_mineralsprings.jpg',0)
img2 = cv2.imread('min.png',0)
img3 = cv2.imread('min.png',0)

# Initiate STAR detector
orb = cv2.ORB_create()


kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

# create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descriptors.
matches = bf.match(des1,des2)

# Sort them in the order of their distance.
matches = sorted(matches, key = lambda x:x.distance)

# Draw first 10 matches.
img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:10],img3,flags=2)

cv2.imshow('image', img3); cv2.waitKey(0)
