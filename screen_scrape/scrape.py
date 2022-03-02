
from PIL import Image
import pytesseract
import cv2
import numpy as np
import json
import datetime


def get_aution_house_prices(screenshot_path, descriptor):
    img = cv2.imread(screenshot_path)
    item_list = img[409:1173, 1246:1641]
    avg_list = img[409:1173, 1651:1828]
    recent_list = img[409:1173, 1894:2044]
    lowest_list = img[409:1173, 2101:2260]
    remaining_list = img[409:1173, 2314:2607]

    response = {}

    items = get_items(item_list)
    avg = get_price_list(avg_list)
    recent = get_price_list(recent_list)
    low = get_price_list(lowest_list)
    remain = get_price_list(remaining_list)

    index = 0
    for item in items:
        response[item] = {}
        response[item]['Average Price'] = avg[index]
        response[item]['Recent Price'] = recent[index]
        response[item]['Lowest Price'] = low[index]
        response[item]['Remaining Items'] = remain[index]
        index += 1

        # datetime object containing current date and time
    screenshot = screenshot_path.split('/')
    file_date = screenshot[1][0:11]

    with open('json_data/market_data-' + descriptor + '-' + file_date + '.json', 'w') as outfile:
        json.dump(response, outfile, indent=4)



def get_items(item_list):
    inv_item_list = cv2.bitwise_not(item_list)
    gray_item_list = cv2.cvtColor(inv_item_list, cv2.COLOR_BGR2GRAY)
    market_items = pytesseract.image_to_string(gray_item_list , config="--oem 3 --psm 4", lang = 'eng')

    market_list = market_items.split('\n')
    item_list = []
    index = -1
    for item in market_list:
        if item == '\x0c' or item.isspace() or item == '':
            pass
        elif item == '[Sold in bundles of 10 units]':
            item_list[index] = item_list[index] + ' (10)'
        else:
            index += 1
            item_list.append(item)

    return item_list

def get_price_list(price_list):
    gray = cv2.cvtColor(price_list, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((4, 1), 'uint8')
    dilate_img = cv2.dilate(gray, kernel, iterations=1)
    reverse = cv2.bitwise_not(dilate_img)
    avg_item_list = pytesseract.image_to_data(reverse , config="--oem 3 --psm 6", lang = 'eng', output_type=pytesseract.Output.DICT)

    price_item_list = []
    for item in avg_item_list['text']:
        if item != '':
            if item == 'i' or item == 'I':
                price_item_list.append(1.0)
            else:
                price_item_list.append(float(item.replace(',', '')))
    
    return price_item_list
