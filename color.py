import cv2
import numpy as np
import sys
import urllib

def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    #import pdb; pdb.set_trace()
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
    # return the image
    return image

#img = url_to_image(sys.argv[1])
img = cv2.imread('17_pongmeivalley.jpg')

RED_MIN_LOW = np.array([0, 210, 210],np.uint8)
RED_MAX_LOW = np.array([5, 255, 255],np.uint8)
RED_MIN_HIGH = np.array([175, 210, 210],np.uint8)
RED_MAX_HIGH = np.array([180, 255, 255],np.uint8)

hsv_img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

frame_threshed_low = cv2.inRange(hsv_img, RED_MIN_LOW, RED_MAX_LOW)
frame_threshed_high = cv2.inRange(hsv_img, RED_MIN_HIGH, RED_MAX_HIGH)
output = cv2.addWeighted(frame_threshed_low, 1.0, frame_threshed_high, 1.0, 0.0)
template = cv2.imread('dot.jpg',0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(output,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.3
loc = np.where( res >= threshold)

# for pt in zip(*loc[::-1]): 
#     cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (255,0,0), 2)

targets = zip(*loc[::-1])
offset = (w/2,h/2)
targets = [tuple(map(sum, zip(target, offset))) for target in targets]

for pt in targets:
	cv2.circle(img, pt, 1, (255, 0, 0))

#output = cv2.GaussianBlur(output,(5,5),0)
cv2.imwrite('output2.jpg', img)
cv2.imshow('image', img); cv2.waitKey(0)