import pyscreenshot as ImageGrab
import PIL
import cv2
import urllib
import numpy as np
import sys
from matplotlib import pyplot as plt

# usage: python match_url_to_screenshot.py http://whatever.com/huh.jpg

# METHOD #1: OpenCV, NumPy, and urllib
def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE) # cv2.imdecode(image, cv2.IMREAD_COLOR)

    # return the image
    return image

im=ImageGrab.grab(bbox=(0,0,1920,1080)) # X1,Y1,X2,Y2
print type(im)
im=im.convert('RGB')
print type(im)
im = np.array(im)
print type(im)

cv_img = im.astype(np.uint8)
#print url_to_image
img = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY)
#template = cv2.imread("filename.png", cv2.IMREAD_GRAYSCALE)

#img = cv2.imread('messi5.jpg',0)
img2 = img.copy()
template = url_to_image(sys.argv[1]) # cv2.imread('template.jpg',0)
print template

w, h = template.shape[::-1]

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

# winners: 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_SQDIFF_NORMED'

for meth in methods:
    img = img2.copy()
    method = eval(meth)

    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv2.rectangle(img,top_left, bottom_right, 255, 2)

    plt.subplot(121),plt.imshow(res,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(template,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)

    plt.show()
