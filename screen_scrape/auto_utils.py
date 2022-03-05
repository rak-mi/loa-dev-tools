import win32gui
from pynput.mouse import Button, Controller

def move_mouse(x,y):

    hwnd = win32gui.FindWindowEx(0,0,0, "LOST ARK (64-bit, DX11) v.2.0.2.1")
    win32gui.SetForegroundWindow(hwnd)
    pos_x = int(x)
    pos_y = int(y)

    mouse = Controller()

    # Read pointer position
    #print('The current pointer position is {0}'.format(
    #    mouse.position))

    # Move pointer relative to current position
    mouse.position = (pos_x, pos_y)

    # Press and release
    mouse.press(Button.left)
    mouse.release(Button.left)

    # Double click; this is different from pressing and releasing
    # twice on Mac OSX
    #mouse.click(Button.left, 2)

    # Scroll two steps down
    #mouse.scroll(0, 2)


def convert_time_into_mari_time(time):
    time_split = time.split('-')
    date = time_split[0]
    time = int(time_split[1])

    if time >= 1 and time < 7:
        return date + '-0100-0700'
    elif time >= 7 and time < 13:
        return date + '-0700-1300'
    elif time >= 13 and time < 19:
        return date + '-1300-1900'
    elif time >= 19 or time == 0:
        return date + '-1900-0100'
    else:
        return date + '-0000-0000'