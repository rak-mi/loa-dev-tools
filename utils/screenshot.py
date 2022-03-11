import win32gui
import win32ui
from ctypes import windll
from PIL import Image
import datetime

def take_screenshot_of_window(type,type_2,mode, w, h):
    hwnd = win32gui.FindWindow(None, 'LOST ARK (64-bit, DX11) v.2.1.0.1')

    # datetime object containing current date and time
    now = datetime.datetime.now(datetime.timezone.utc)
    dt_string = now.strftime("%d%m%Y-%H%M")

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, int(w), int(h))

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
        im.save('screenshots/' + type + '/'  + type_2 + '-' + mode + '-' + dt_string + '.png')

    return('market_data/' + dt_string + '-screenshot.png')