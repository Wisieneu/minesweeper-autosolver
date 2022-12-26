import cv2 as cv
from cv2 import TM_CCOEFF_NORMED
from tools.funcstorage import window_capture
import numpy as np
import pyautogui, win32gui, time, os, win32com.client
from tools.funcstorage import (Buttons, Assets, get_grid, freeze_get_inputkey, 
                               clear_console, detect_version)
import random

# TO DO:
#  For loop checking each tile's number/status/properties and updating their status (even in between moves later) 
#  Learn how to match RECTANGLES to IMAGES ASAP
#  Loop whole grid searching for a number that's fulfilled 
#
#  Click randomly until a 100% bomb tile is discovered, if failed keep trying again 
#  Figure out a way to unstuck when no 100% move is available



MS_window = None
while not MS_window:
    clear_console()
    print('''        The program first needs to focus Minesweeper's window.
        Please make sure you have a client/web version on.\n
    Press [ 1 ] to continue\n''')

    inputkey = freeze_get_inputkey()
    match inputkey.lower():
        case '1':
            pass
        case _:
            continue

    try: # grabs focus of a minesweeper client if able to find it
        MS_window = win32gui.FindWindow(None, 'Minesweeper')
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%') #for some reason ALT key is needed not to crash
        win32gui.SetForegroundWindow(MS_window)
        print('''    Found a minesweeper "{}" window.
    Do dot move it from now on.\n'''.format(MS_window))
        # TBD alt-tabbing to this window
        clear_console(1.5)
        break
    
    except:
        while True:
            print('''    Unable to find a minesweeper window
        switch to it manually and do not move it
        if you are using a web browser try not to mess with zoom settings\n
    Press [ 1 ] to continue\n''')
            MS_window = None
            inputkey = freeze_get_inputkey()
            match inputkey.lower():
                case '1':
                    clear_console()
                    break
                case _:
                    continue
        break


match detect_version():
    case 'windows':
        windowsxpver_assets_dir = os.path.normpath(r'tools\assets\windowsxpver')
        windowsxpver_assets_filenames = [img for img in os.listdir(windowsxpver_assets_dir) if img.endswith(".jpg")]
        assetsInstances = {}
        for filename in windowsxpver_assets_filenames:
            assetsInstances[filename] = Assets(os.path.join(windowsxpver_assets_dir, filename))
            pass
        print(assetsInstances)
        print(assetsInstances[windowsxpver_assets_filenames[0]])
    case 'googlever':
        windowsxpver_assets_dir = os.path.normpath(r'tools\assets\googlever')
            





source_img = np.array(window_capture())
source_gray = cv.cvtColor(source_img, cv.COLOR_BGR2GRAY)
square = cv.imread(r'tools\assets\windowsxpver\uncovered.jpg', cv.IMREAD_UNCHANGED)
square_gray = cv.cvtColor(square, cv.COLOR_BGR2GRAY)
square_size = square.shape

#   creates a new source_img copy of black-grey-white pixels, 
#   where black is the most unlikely match and perfect whtite is a 100% match
result = cv.matchTemplate(source_gray, square_gray, TM_CCOEFF_NORMED)
#   these return a list of coordinates that program matches 
#   with a confidence of at least 80%
detections = np.where(result >= 0.80)
detections = list(zip(detections[1], detections[0]))
print(detections)

#   figure out what type of XY grid it is based on coordinates of detections
try:
    grid = get_grid(detections, square_size)
except:
    print('''Cannot find any squares, please restart the program
if the issue persists, contact Wisie on GitHub''')
X_list = []
Y_list = []
for x,y in detections:
    if x not in X_list: X_list.append(x)
    if y not in Y_list: Y_list.append(y)

#   transforms square detections to class objects 
for top_left in detections:
    xy = (X_list.index(top_left[0])+1, Y_list.index(top_left[1])+1)
    bottom_right = (top_left[0] + square_size[0], top_left[1] - square_size[1])
    Buttons(top_left, bottom_right, xy)
    cv.rectangle(source_img, top_left, (top_left[0]+square_size[0], top_left[1]+square_size[1]), (0,255,0), thickness=2, lineType=cv.LINE_4)





print('end')
time.sleep(10)
exit()