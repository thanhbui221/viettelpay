import math
from operator import truediv
import pyautogui
# import pydirectinput
import cv2
import os
import threading
from time import time
import numpy as np
from windowcapture import WindowCapture
from time import time
from math import *

wincap = WindowCapture("LDPlayer")
target_x = wincap.obj_x
target_y = wincap.obj_y
print(wincap.h)
paddle_y = target_y - 40
height = wincap.h

# running = True
# def predict_move(delta, circles1, circles):
    # # sau khi tinh toan, thi tu khi lan capture1 den khi vien dan bay xuong bottom man hinh la 4,5 lan capture. 
    # # tinh quy dao o lan capture thu 4 de ne
    # # circles1 va circles2 co thu tu cac vien dan giong nhau 
    # # t1, circles1: xt1, yt1
    # # t2, circles2: xt2, yt2
    # for pt in circles1[0, :]:
    #     x, y, r = pt[0], pt[1], pt[2]
    #     # cv2.circle(scr, (x, y), r, (0, 0, 255), 5)
    #     ball_x = x
    #     ball_y = y

# t = threading.Thread(target=move_target)
# t.start()
delta = time()
first_time = True

# print(target_x, target_y)
# pyautogui.moveTo(target_x, target_y)
# first_time = True
catch_count = 0
circles_next = None
while True:
    scr = wincap.get_screenshot()

    # Capture 0,0 -> w, 300
    cv2.rectangle(scr, (0, 0), (wincap.w, 300), (0,0,0), -1) 

    # Cai nay lam gi a
    gray = cv2.cvtColor(scr, cv2.COLOR_BGR2GRAY)


    circles = circles_next
    # cai function cs2.HoughCircles bat dc cac hinh tron
    # khi anh cap cho no o dang xam
    
    circles_next = cv2.HoughCircles(
        gray, cv2.HOUGH_GRADIENT,
        1, 20,
        param1=50, param2=30,
        minRadius=40, maxRadius=50)

    # because we catch the lower 3/4 of the screen, therefore, it will always catch the bullets.
    
    # if not exists c1, c2 then continue to next loop
    try:
        c1 = circles[0, :]
        c2 = circles_next[0, :]
    except Exception as e:
        continue
    
    if c1 and c2:
        print("start")
        l = []
        for pt1 in c1:
            for pt2 in c2:
                l.append([(pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2, pt1, pt2])
                            # [ sqrt((x1-x2)^2 + (y1-y2)^2), [x1, y1], [x2, y2] ]
                            # l co the la list cac dict, dict co key la distance
        pair = []
        ok = [] 
        l.sort(key=lambda x: x[0]) 
        # l = [(123, [x1, y1], [x2, y2]), (123, {"x": 4, "y": 5}), (123, {"x": 4, "y": 5})]
        for d in l:
            if d[1] not in ok and d[2] not in ok:
                pair.append((d[1], d[2]))
                ok.extend([d[1], d[2]])
                # pair: typle các cặp có label giống nhau
                # ok: các viên đạn đã được ghép cặp
                # ở đây em loại trừ dần dần, 2 điểm gần nhất: p1 ở c1, p2 ở c2 coi chúng là 1 cặp 
                
        
    
    
    # if circles_next is not None and circles is not None:
    #     delta = time() - delta
        
    #     if delta < 0.1:
    #         catch_count += 1
    #         for pt1, pt2 in zip(circles[0, :], circles_next[0, :]):
    #             x1, y1, r1 = pt1[0], pt1[1], pt1[2]
    #             x2, y2, r2 = pt2[0], pt2[1], pt2[2]
                                    
    #             if x2 > x1: 
    #                 delta_ball_x = x2 - x1
    #             else:
    #                 delta_ball_x = x1 - x2
                    
    #             delta_ball_y = y2 - y1
    #             if catch_count == 3:
    #                 if x2 > x1:
    #                     predict_x = x2 + delta_ball_x *  3
    #                 else:
    #                     predict_x = x2 - delta_ball_x * 3
    #                 predict_y = y2 + delta_ball_y * 3
    #                 print("Predict_x", predict_x)     
    #                 print("Predict_y", predict_y)           
    #     else:
    #         circles = []
    #         catch_count = 0
        
        delta = time()    

    cv2.imshow('output', scr)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        running = False
        break