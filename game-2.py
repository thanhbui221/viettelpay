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

def sqrdist(pt1, pt2):
    return sqrt((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)

def area(pt1, pt2, pt3):
    l1 = sqrdist(pt1, pt2)
    l2 = sqrdist(pt2, pt3)
    l3 = sqrdist(pt3, pt1)
    p = (l1 + l2 + l3)/2
    area = sqrt(p * (p - l1) * (p - l2) * (p - l3))
    return area 
    
cList = {}
    
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
        print(len(c1))
        print(len(c2))        
    except Exception as e:
        continue # case not valid c1, c2

    try:
        print("start")
        l = []
        for pt1 in c1:
            for pt2 in c2:
                l.append([sqrdist(pt1, pt2), pt1, pt2])
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
                
                p = False
                for c in cList:
                    if d[1] in cList[c]:
                        p = True
                        cList[c].append(d[2])
                if p == False:
                    cList[d[1]] = [d[1], d[2]]
    except Exception as e:
        print(e)
    countC = 0
    for c in cList:
        countC += 1
        p = True
        for i in range(len(cList[c])):
            for j in range(i+1, cList[c]):
                for k in range(j+1, cList[c]):
                    pt1 = cList[c][i]
                    pt2 = cList[c][j]
                    pt3 = cList[c][k]
                    eps = 1e-3
                    if area(pt1, pt2, pt3) > eps:
                        p = False
        
        # p == True: straight //  p != True: curve
        print(f"{countC}: Label {p}, List points {cList[c]}")
                
    
    cv2.imshow('output', scr)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        running = False
        break