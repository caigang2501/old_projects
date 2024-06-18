


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

pytesseract.pytesseract.tesseract_cmd = r'D:/Program Files/Tesseract-OCR/tesseract.exe'

JUDGEMENTONEDIM = 15
JUDGEMENTRGB = 20
JUDGEMENTTOLTALG = 90
JUDGEMENTG = 150
JUDGEMENTDARK = 170

def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)

def send(s):
    pyautogui.keyDown(s)
    time.sleep(0.1)
    pyautogui.keyUp(s)

def getmouseposandcolor():
    pyautogui.displayMousePosition()

def getposcolor(x,y):
    return pyautogui.pixel(x,y)[0]

def getsamecolor(path,kw,kh):
    ndarray = cv.imread(path, 0)
    barr = np.zeros((len(ndarray),len(ndarray[0])))
    for i in np.arange(len(ndarray)-kh+1):
        for j in np.arange(len(ndarray[0])-kw+1):
            temp = ndarray[i:i+kh,j:j+kw]
            m = 0
            # 求temp方差
            m += sum(sum(abs(np.ones((kh,kw))*temp.mean()-temp)))
            if m < JUDGEMENTONEDIM: 
                barr[i:i+kh,j:j+kw] = np.ones((kh,kw))*255
    return barr

def getsamecolorRGB(path,kw,kh):
    ndarray = cv.imread(path, 1)
    barr = np.zeros((len(ndarray),len(ndarray[0]),3))
    for i in np.arange(len(ndarray)-kh+1):
        for j in np.arange(len(ndarray[0])-kw+1):
            temp = ndarray[i:i+kh,j:j+kw]
            m = 0
            # 求temp方差
            for x in range(3):
                pis = temp[:,:,x]
                # 求pis方差
                m += sum(sum(abs(np.ones((kh,kw))*pis.mean()-pis)))
            if m < JUDGEMENTRGB:    
                barr[i:i+kh,j:j+kw,:] = np.ones((kh,kw,3))*255
    return barr

def getsamecolorG(path,kw,kh):
    ndarray = cv.imread(path, 1)
    barr = np.zeros((len(ndarray),len(ndarray[0]),3))
    for i in np.arange(len(ndarray)-kh+1):
        for j in np.arange(len(ndarray[0])-kw+1):
            temp = ndarray[i:i+kh,j:j+kw,1]
            m = 0
            # 求temp方差
            m += sum(sum(abs(np.ones((kh,kw))*temp.mean()-temp)))
            if m < JUDGEMENTRGB:    
                barr[i:i+kh,j:j+kw,:] = np.ones((kh,kw,3))*255
    return barr

def gettotalcolorG(path,kw,kh):
    ndarray = cv.imread(path, 1)
    barr = np.zeros((len(ndarray),len(ndarray[0]),3))
    for i in np.arange(len(ndarray)-kh+1):
        for j in np.arange(len(ndarray[0])-kw+1):
            temp = ndarray[i:i+kh,j:j+kw,1]
            m = 0
            m += sum(sum(temp))//(kw*kh)
            if m > JUDGEMENTTOLTALG:    
                barr[i:i+kh,j:j+kw,:] = np.ones((kh,kw,3))*255
    return barr

def gettopcolorG(path):
    im = Image.open(path)
    image=im.resize((im.width*30//10,im.height*30//10))
    image.save('gamescripts/120.jpg')
    ndarray = cv.imread('gamescripts/120.jpg', 1)
    barr = np.zeros((len(ndarray),len(ndarray[0]),3))
    for i in np.arange(len(ndarray)):
        for j in np.arange(len(ndarray[0])):
            if ndarray[i][j][1] > JUDGEMENTG:    
                barr[i,j] = np.ones((3))*255
    return barr

def gettopcolorDark(path):
    im = Image.open(path)
    image=im.resize((im.width*20//10,im.height*20//10))
    image.save('gamescripts/111.jpg')
    ndarray = cv.imread(path, 1)
    barr = np.zeros((len(ndarray),len(ndarray[0]),3))
    for i in np.arange(len(ndarray)):
        for j in np.arange(len(ndarray[0])):
            if sum(ndarray[i][j])//3 > JUDGEMENTDARK:    
                barr[i,j] = np.ones((3))*255
    return barr


im = Image.open('gamescripts/11.jpg')
image=im.resize((im.width*15//10,im.height*15//10))
image.save('gamescripts/111.jpg')
# png = gettopcolorDark('gamescripts/110.jpg')
# cv.imwrite('gamescripts/111.jpg',png)
print(pytesseract.image_to_string('gamescripts/111.jpg',lang='chi_sim'))

# def getsamecolorRGB(path:np.ndarray,kw,kh):
#     ndarray = cv.imread(path, 1)
#     barr = np.zeros((len(ndarray),len(ndarray[0])))
#     for i in np.arange(len(ndarray)-kh+1):
#         for j in np.arange(len(ndarray[0])//3-kw+1):
#             temp = ndarray[i:i+kh,j:j+kw*3].T
#             m = 0
#             tr = len(temp)
#             for x in range(3):
#                 rows = (np.arange(kw*3) % 3) == x
#                 pis = temp[rows]
#                 # 求pis方差
#                 m += sum(sum(abs(np.ones((kh,kw))*pis.mean()-pis)))
#             if m < JUDGEMENTRGB:    
#                 tt = barr[i:i+kh,j*3:(j+kw)*3]
#                 barr[i:i+kh,j*3:(j+kw)*3] = np.ones((kh,kw*3))*255
#     return barr
# png = getsamecolor('gamescripts/12.jpg',2,2)
# png = gettopcolorG('gamescripts/12.jpg')
# cv.imwrite('gamescripts/121.jpg',png)
# plt.imshow(png[:,:,::-1])
# plt.show()


# while keyboard.is_pressed('q') == False:
 
#     time.sleep(1)

# keyboard.wait('1')
# img = pyautogui.screenshot(region=(0,0,1919,1079))
# img.save("gamescripts/pyscreenshot.jpg")
# npimg = cv.imread('gamescripts/pyscreenshot.jpg',1)
# plt.imshow(npimg[:,:,::-1])
# # 灰度图
# plt.imshow(npimg,cmap=plt.cm.gray)
# plt.show()

# pyautogui.locateOnScreen("gamescripts/npc1.jpg",grayscale=True,confidence=0.8)

#膨胀
# path = 'gamescripts/lol.jpg'
# png = cv.imread(path, 0) #(0:单通道 1:3通道) return np.ndarray
# kernel = cv.getStructuringElement(cv.MORPH_RECT,(2, 2))
# eroded = cv.erode(png, kernel)
# cv.imwrite('gamescripts/121.jpg',eroded)



#放大
# im = Image.open('gamescripts/12.jpg')
# image=im.resize((im.width*15//10,im.height*15//10))
# image.save('gamescripts/121.jpg')

# path = 'gamescripts/11.jpg'
# png = cv.imread(path, 1)
# png = png[:,:-2]
# newpng = np.zeros((len(png),len(png[0])))
# kw,kh = 2,2
# print(newpng.shape)


# with open("gamescripts/text.txt", "w") as out_file:
#     out_file.write(pytesseract.image_to_string('gamescripts/pyscreenshot.jpg',lang='chi_sim'))
# pyautogui.displayMousePosition()

# def mycall():
#     x,y,w,h = pyautogui.locateOnScreen("gamescripts/npc1.jpg",grayscale=True,confidence=0.8)
#     pyautogui.moveTo(x,y)
# keyboard.on_press_key("f4",lambda e:mycall())
# keyboard.wait("esc")





