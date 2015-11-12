import cv2
import numpy as np
import pyscreenshot as ImageGrab


class Player:

    def __init__(self, x=0, y=0, scale=0):
        self.x = x
        self.y = y
        self.scale = scale

    @classmethod
    def calibrate(cls, img_location):
        img = cv2.imread(img_location)
        img2 = img.copy()
        im = ImageGrab.grab(bbox=(20, 97, 1050, 1024))  # X1,Y1,X2,Y2
        print type(im)
        im = im.convert('RGB')
        print type(im)
        im = np.array(im)
        print type(im)
        cv_img = im.astype(np.uint8)
        # print type(cv_img)
        player_map = cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR)
        method = cv2.TM_CCOEFF
        best_quality = 0
        best_scale = 0
        best_x = 0
        best_y = 0

        # brute force to find the scaling factor between user map and solution map
        for scale in np.arange(0.1, 0.5, 0.01):
            template = player_map.copy()
            template = cv2.resize(template, (0, 0), fx=scale, fy=scale)
            w, h = template.shape[1::-1]
            img = img2.copy()
            try:
                res = cv2.matchTemplate(img, template, method)
            except:
                print 'Failed at scale %s' % (scale)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            quality = max_val / abs(cv2.mean(res)[0])
            if quality > best_quality:
                best_quality = quality
                best_scale = scale
                best_x = max_loc[0] + w / 2
                best_y = max_loc[1] + h / 2

        return cls(best_x, best_y, best_scale)
