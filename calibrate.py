import cv2
from matplotlib import pyplot as plt
import numpy as np

def calibrate():
	img = cv2.imread('17_pongmeivalley.jpg')
	# img = cv2.imread('044_mineralsprings.jpg')
	img2 = img.copy()
	# All the 6 methods for comparison in a list
	methods = [ 'cv2.TM_CCOEFF']# , 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
	            # 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
	best_quality = 0
	best_scale = 0
	for scale in np.arange(0.2,0.5,0.01):
	    template = cv2.imread('pong.png')

	    template = cv2.resize(template,(0,0), fx=scale, fy=scale)

	    w, h = template.shape[1::-1]


	    # winners: 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_SQDIFF_NORMED'
	    for meth in methods:
	        img = img2.copy()
	        method = eval(meth)

	        # Apply template Matching
	        res = cv2.matchTemplate(img,template,method)
	        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	        quality = max_val/abs(cv2.mean(res)[0])
	        #print max_val, "avg: ", cv2.mean(res), quality
	        if quality > best_quality:
	            best_quality = quality
	            best_scale = scale

	        # if the method is tm_sqdiff or tm_sqdiff_normed, take minimum
	        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
	            top_left = min_loc
	        else:
	            top_left = max_loc
	        bottom_right = (top_left[0] + w, top_left[1] + h)

	        cv2.rectangle(img,top_left, bottom_right, 255, 2)

	# scale = best_scale
	# template = cv2.imread('pong.png',0)
	# template = cv2.resize(template,(0,0), fx=scale, fy=scale)
	# w, h = template.shape[::-1]
	# for meth in methods:
	    # img = img2.copy()
	    # method = eval(meth)

	    # # apply template matching
	    # res = cv2.matchtemplate(img,template,method)
	    # min_val, max_val, min_loc, max_loc = cv2.minmaxloc(res)

	        # plt.subplot(121),plt.imshow(res,cmap = 'gray')
	        # plt.title(scale), plt.xticks([]), plt.yticks([])
	        # plt.subplot(122),plt.imshow(img,cmap = 'gray')
	        # plt.title('detected point'), plt.xticks([]), plt.yticks([])
	        # plt.suptitle(meth)

	        # plt.show()

	scale = best_scale
	template = cv2.imread('pong.png')
	template = cv2.resize(template,(0,0), fx=scale, fy=scale)
	w, h = template.shape[1::-1]
	for meth in methods:
	    img = img2.copy()
	    method = eval(meth)

	    # apply template matching
	    res = cv2.matchTemplate(img,template,method)
	    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
	    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
	        top_left = min_loc
	    else:
	        top_left = max_loc
	    x = top_left[0]
	    y = top_left[1]
	    bottom_right = (top_left[0] + w, top_left[1] + h)
	    cv2.rectangle(img,top_left, bottom_right, 255, 2)
	    #print template.shape
	    img[y:y+h, x:x+w] = template

	    player.x = 1
	    player.y = 2
	    # plt.subplot(121),plt.imshow(res,cmap = 'gray')
	    # plt.title(scale), plt.xticks([]), plt.yticks([])
	    # plt.subplot(122),plt.imshow(img,cmap = 'gray')
	    # plt.title('detected point'), plt.xticks([]), plt.yticks([])
	    # plt.suptitle(meth)

	    # plt.show()


	#print "best quality:", best_quality
	print best_scale
