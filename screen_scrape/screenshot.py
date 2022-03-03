import win32gui
import win32ui
from ctypes import windll
from PIL import Image
from datetime import datetime

def take_screenshot_of_window(window_name):
    hwnd = win32gui.FindWindow(None, 'LOST ARK (64-bit, DX11) v.2.0.2.1')

    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y-%H")
 
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    #change dimensions to match your resolution
    w = 3440
    h = 1440

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        im.save('market_data/' + dt_string + '-screenshot.png')

    return('market_data/' + dt_string + '-screenshot.png')