import win32gui
from pynput.mouse import Button, Controller

def move_mouse():

    hwnd = win32gui.FindWindowEx(0,0,0, "LOST ARK (64-bit, DX11) v.2.0.2.1")
    win32gui.SetForegroundWindow(hwnd)

    mouse = Controller()

    # Read pointer position
    print('The current pointer position is {0}'.format(
        mouse.position))

    # Move pointer relative to current position
    mouse.move(5, -5)

    # Press and release
    mouse.press(Button.left)
    mouse.release(Button.left)

    # Double click; this is different from pressing and releasing
    # twice on Mac OSX
    mouse.click(Button.left, 2)

    # Scroll two steps down
    mouse.scroll(0, 2)