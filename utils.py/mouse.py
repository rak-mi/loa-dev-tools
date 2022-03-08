import win32gui
from pynput.mouse import Button, Controller
import argparse

def move_mouse(x,y):

    hwnd = win32gui.FindWindowEx(0,0,0, "LOST ARK (64-bit, DX11) v.2.0.3.1")
    win32gui.SetForegroundWindow(hwnd)
    pos_x = int(x)
    pos_y = int(y)

    mouse = Controller()
    mouse.position = (pos_x, pos_y)

    # Press and release
    mouse.press(Button.left)
    mouse.release(Button.left)


parser = argparse.ArgumentParser(description='nah')
parser.add_argument('-x', metavar='t', type=str, help='X position')
parser.add_argument('-y', metavar='p', type=str, help='Y position')
args = parser.parse_args()

move_mouse(args.x, args.y)
