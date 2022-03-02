
from PIL import Image
import pytesseract
import cv2
import numpy as np

def get_aution_house_prices(screenshot_path):
    img = cv2.imread(screenshot_path)
    item_list = img[409:1173, 1246:1641]
    avg_list = img[409:1173, 1651:1828]
    print(get_items(item_list))
    print(get_avg_prices(avg_list))


def get_items(item_list):
    inv_item_list = cv2.bitwise_not(item_list)
    gray_item_list = cv2.cvtColor(inv_item_list, cv2.COLOR_BGR2GRAY)
    market_items = pytesseract.image_to_string(gray_item_list , config="--oem 3 --psm 4", lang = 'eng')
    
    return market_items

def get_avg_prices(avg_list):
    gray = cv2.cvtColor(avg_list, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((4, 1), 'uint8')
    dilate_img = cv2.dilate(gray, kernel, iterations=1)
    reverse = cv2.bitwise_not(dilate_img)
    avg_item_list = pytesseract.image_to_string(reverse , config="--oem 3 --psm 6", lang = 'eng')

    return avg_item_list
