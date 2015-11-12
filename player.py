import cv2
import numpy as np


class Player:
    def __init__(self, x=0, y=0, scale=0):
        self.x = x
        self.y = y
        self.scale = scale

    @classmethod
    def calibrate(cls, img_location):
        img = cv2.imread(img_location)
        img2 = img.copy()
        method = cv2.TM_CCOEFF
        best_quality = 0
        best_scale = 0
        best_x = 0
        best_y = 0
        # brute force to find the scaling factor between user map and solution map
        for scale in np.arange(0.2, 0.5, 0.01):
            template = cv2.imread('pong.png')
            template = cv2.resize(template, (0, 0), fx=scale, fy=scale)
            w, h = template.shape[1::-1]
            img = img2.copy()

            res = cv2.matchTemplate(img, template, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            quality = max_val / abs(cv2.mean(res)[0])
            if quality > best_quality:
                best_quality = quality
                best_scale = scale
                best_x = max_loc[0] + w / 2
                best_y = max_loc[1] + h / 2

        return cls(best_x, best_y, best_scale)
