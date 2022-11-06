import pyautogui, numpy, msvcrt, time, os
# clears console, can be delayed by an argument integer 
def clear_console(delay=0):
    time.sleep(delay)
    os.system('cls')

# stops the program until it receives an input, then held in inputKey variable
def freeze_wait_for_input():
    input_key = msvcrt.getch().decode('utf-8')
    return input_key
    
#takes a screenshot of a specific window; if None will just screenshot whole primary screen 
def window_capture(window=None):
    import win32gui, win32ui, win32con


    if window:
        hwnd = win32gui.FindWindow(None, str(window))
        window_nr = win32gui.FindWindow(None, str(window))
        window_rect = win32gui.GetWindowRect(window_nr)
        w, h = window_rect[2] - window_rect[0], window_rect[3] - window_rect[1]
    #if window is not detected, it will just use a screenshot
    else:
        hwnd = None
        w, h = pyautogui.size()
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj=win32ui.CreateDCFromHandle(wDC)
    cDC=dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)

    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = numpy.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    img = img[...,:3]
    
    return img