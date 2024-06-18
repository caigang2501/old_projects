

import pyautogui
import win32api,win32con
import time
import keyboard
import numpy as np
import random
import matplotlib.pyplot as plt
import cv2 as cv
from PIL import Image

import pytesseract

JUDGEMENTG = 150
JUDGEMENTBAI = 120



def gettopcolorG(path):
    im = Image.open(path)
    image=im.resize((im.width*30//10,im.height*30//10))
    image.save('moyu/120.jpg')
    ndarray = cv.imread('moyu/120.jpg', 1)
    barr = np.zeros((len(ndarray),len(ndarray[0]),3))
    for i in np.arange(len(ndarray)):
        for j in np.arange(len(ndarray[0])):
            if ndarray[i][j][1] > JUDGEMENTG:    
                barr[i,j] = np.ones((3))*255
    return barr

def gettopcolorBAI(path):
    im = Image.open(path)
    image=im.resize((im.width*30//10,im.height*30//10))
    image.save('moyu/taskbai.jpg')
    ndarray = cv.imread('moyu/taskbai.jpg', 1)
    barr = np.zeros((len(ndarray),len(ndarray[0]),3))
    for i in np.arange(len(ndarray)):
        for j in np.arange(len(ndarray[0])):
            if sum(ndarray[i][j][:])//3 > JUDGEMENTBAI:    
                barr[i,j] = np.ones((3))*255
    return barr

def choosetask():
    print(1)

# pictaskkind = gettopcolorBAI('moyu/taskkind.jpg')
# cv.imwrite('moyu/taskbai.jpg',pictaskkind)
# print(pytesseract.image_to_string('moyu/taskkind.jpg',lang='chi_sim'))

boxarr = pyautogui.locateAllOnScreen("moyu/blood1.jpg",grayscale=True,confidence=0.8)
print(boxarr)

def mycall():
    boxarr = pyautogui.locateAllOnScreen("moyu/blood1.jpg",grayscale=True,confidence=0.8)
    print(boxarr.)

keyboard.on_press_key("f4",lambda e:mycall())
keyboard.wait("esc")

