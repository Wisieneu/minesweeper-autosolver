import cv2 as cv
from cv2 import TM_CCOEFF_NORMED
from tools.funcstorage import window_capture
import numpy as np
import pyautogui, win32gui, time, os
from tools.funcstorage import freeze_wait_for_input, clear_console


# TO DO:
#  For loop checking each tile's number/status/properties and updating their status (even in between moves later) 
#  Learn how to match RECTANGLES to IMAGES ASAP
#  Loop whole grid searching for a number that's fulfilled 
#
#  Click randomly until a 100% bomb tile is discovered, if failed keep trying again 
#  Figure out a way to unstuck when no 100% move is available



class Buttons:
    button_list = []
    def __init__(self, top_left, bottom_right, xy):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.midpoint = (top_left[0]+bottom_right[0]//2, top_left[1]+bottom_right[1]//2)
        self.width = self.bottom_right[0]-self.top_left[0]
        self.height = self.bottom_right[1]-self.top_left[1]
        self.xy = xy
        self.status = 'uncovered'
        self.button_list.append(self)

    def check_if_matches(self, obj):
        pass
    
    def check_surroundings(self):
        #up down right left and corners fastest loop possible ASAP
        pass

    def click_button(self, which_button='left'):
        pyautogui.click(button=which_button.upper(), x=self.midpoint[0], y=self.midpoint[1])

def detect_version():
    pass #tbd when winxp ver is done

def find_instance(xy):
    for obj in Buttons.button_list:
        if obj.xy == xy: 
            return obj





MS_window = None
while not MS_window:
    clear_console()
    print('''\n        The program first needs to detect Minesweeper's window.
    Please focus the game's client now.\n
    Press [ 1 ] to continue''')

    inputkey = freeze_wait_for_input()
    match inputkey.lower():
        case '1':
            pass
        case 'q':
            exit()
        case _:
            continue
    
    try:
        MS_window = win32gui.FindWindow(None, 'Minesweeper')
        print('    Found a minesweeper "{}" window'.format(MS_window))
        screenshot = window_capture('minesweeper')

    except:
        print('''Unable to find a minesweeper window
                switch to it manually and do not move it''')
        MS_window = None
        screenshot = window_capture()



source_img = np.array(screenshot)
source_gray = cv.cvtColor(source_img, cv.COLOR_BGR2GRAY)
square = cv.imread(r'minesweeper\assets\windowsxpver\uncovered.jpg', cv.IMREAD_UNCHANGED)
square_gray = cv.cvtColor(square, cv.COLOR_BGR2GRAY)
square_size = square.shape

#   creates a new source_img copy of black-grey-white pixels, 
#   where black is the most unlikely match and perfect whtite is a 100% match
result = cv.matchTemplate(source_gray, square_gray, TM_CCOEFF_NORMED)
#   these return a list of coordinates that program matches 
#   with a confidence of at least 80%
detections = np.where(result >= 0.80)
detections = list(zip(detections[1], detections[0])) # REMEMBER THAT 1ST IS Y AND 2ND IS X (WHO THE ACTUAL F INVENTED THIS I SPENT 2H DEBUGGING THIS WANTING TO DROP)
print(detections)

X_list = []
Y_list = []
for x,y in detections:
    if x not in X_list: X_list.append(x)
    if y not in Y_list: Y_list.append(y)

print(X_list, type(X_list))
print(Y_list)
#   figure out what type of XY grid it is based on coordinates of detections
first = detections[0]
last = detections[-1]

grid = (((detections[-1][0] - detections[0][0])//square_size[1])+1, # X
        ((detections[-1][1] - detections[0][1])//square_size[0])+1)  # Y
print('a XY {} grid type detected'.format(grid))

#   creates squares as class objects 
for top_left in detections:
    xy = (X_list.index(top_left[0])+1, Y_list.index(top_left[1])+1)
    bottom_right = (top_left[0] + square_size[0], top_left[1] - square_size[1])
    Buttons(top_left, bottom_right, xy)
    cv.rectangle(source_img, top_left, (top_left[0]+square_size[0], top_left[1]+square_size[1]), (0,255,0), thickness=2, lineType=cv.LINE_4)




cv.imshow('test', source_img)
cv.waitKey(1500)
cv.destroyAllWindows()





print('''===================  TASK DONE  ===================''')
time.sleep(3)