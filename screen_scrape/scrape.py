
from PIL import Image
import pytesseract
import cv2
import numpy as np
import json
import datetime


def get_aution_house_prices(screenshot_path, descriptor, file_date):
    img = cv2.imread(screenshot_path)
    item_list = img[409:1173, 1246:1641]
    avg_list = img[409:1173, 1651:1828]
    recent_list = img[409:1173, 1894:2044]
    lowest_list = img[409:1173, 2101:2260]
    #remaining_list = img[409:1173, 2314:2597]

    response = {}

    
    items = get_items(item_list)
    avg = get_price_list(avg_list)
    if len(avg) != len(items):
        avg = get_price_list2(avg_list)
    recent = get_price_list(recent_list)
    if len(recent) != len(items):
        recent = get_price_list2(recent_list)
    low = get_price_list(lowest_list)
    if len(low) != len(items):
        low = get_price_list2(lowest_list)

    #remain = get_price_list(remaining_list)

    index = 0
    for item in items:
        response[item] = {}
        response[item]['Average Price'] = avg[index]
        response[item]['Recent Price'] = recent[index]
        response[item]['Lowest Price'] = low[index]
        response[item]['Remaining Items'] = 100
        index += 1

        # datetime object containing current date and time
    
    return response

    #with open('json_data/market_data-' + descriptor + '-' + file_date + '.json', 'w') as outfile:
    #    json.dump(response, outfile, indent=4)



def get_mari_prices(screenshot_path, descriptor, mari_slot):
    img = cv2.imread(screenshot_path)
    item_list = img[591:1291, 2295:2749]
    price_list = img[642:1283, 2785:2881]

    items = get_items(item_list)
    prices = get_price_list(price_list)

    #load mari json conversion
    with open('json_data/translate-mari-abriviation.json', 'r') as outfile:
        mari_data = json.load(outfile)

    data = {}
    data[mari_slot] = {}
    for x in range (0,6):
        item = items[x] + ' - ' + str(int(prices[x]))
        mari_item = mari_data[item]['name']
        mari_price = mari_data[item]['price']
        mari_ammount = mari_data[item]['ammount']

        data[mari_slot][mari_item] = { "ammount": mari_ammount, "price": mari_price }

    return data


def get_currency_exchange(screenshot_path, descriptor):
    img = cv2.imread(screenshot_path)
    price_list = img[403:743, 1896:1972]
    prices = get_currency_list(price_list)
    avg_price = sum(prices) / len(prices)
    return (avg_price)

def get_items(item_list):
    inv_item_list = cv2.bitwise_not(item_list)
    gray_item_list = cv2.cvtColor(inv_item_list, cv2.COLOR_BGR2GRAY)
    market_items = pytesseract.image_to_string(gray_item_list , config="--oem 3 --psm 4", lang = 'eng')

    #for testing, below code will show which section is being cropped
    #cv2.imshow('dilate', reverse)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


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

    #print(item_list)
    return item_list

def get_price_list(price_list):
    gray = cv2.cvtColor(price_list, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((5, 3), 'uint8')
    dilate_img = cv2.dilate(gray, kernel, iterations=1)
    reverse = cv2.bitwise_not(dilate_img)

    # for testing, below code will show which section is being cropped
    #cv2.imshow('dilate', reverse)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    avg_item_list = pytesseract.image_to_data(reverse , config="--oem 3 --psm 6", lang = 'eng', output_type=pytesseract.Output.DICT)
    #print (avg_item_list['text'])
    price_item_list = []
    for item in avg_item_list['text']:
        if item != '':
            if item == 'i' or item == 'I':
                price_item_list.append(1.0)
            else:
                price_item_list.append(float(item.replace(',', '')))
    
    return price_item_list

def get_price_list2(price_list):
    gray = cv2.cvtColor(price_list, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((4, 2), 'uint8')
    dilate_img = cv2.dilate(gray, kernel, iterations=1)
    reverse = cv2.bitwise_not(dilate_img)

    # for testing, below code will show which section is being cropped
    #cv2.imshow('dilate', reverse)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    avg_item_list = pytesseract.image_to_data(reverse , config="--oem 3 --psm 6", lang = 'eng', output_type=pytesseract.Output.DICT)
    #print (avg_item_list['text'])
    price_item_list = []
    for item in avg_item_list['text']:
        if item != '':
            if item == 'i' or item == 'I':
                price_item_list.append(1.0)
            else:
                price_item_list.append(float(item.replace(',', '')))
    
    return price_item_list

def get_currency_list(price_list):
    gray = cv2.cvtColor(price_list, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((4, 2), 'uint8')
    dilate_img = cv2.dilate(gray, kernel, iterations=1)
    reverse = cv2.bitwise_not(dilate_img)

    # for testing, below code will show which section is being cropped
    #cv2.imshow('dilate', reverse)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    avg_item_list = pytesseract.image_to_data(reverse , config="--oem 3 --psm 4", lang = 'eng', output_type=pytesseract.Output.DICT)
    #print (avg_item_list['text'])
    price_item_list = []
    for item in avg_item_list['text']:
        if item != '':
            if item == 'i' or item == 'I':
                price_item_list.append(1.0)
            else:
                price_item_list.append(float(item.replace(',', '')))
    
    return price_item_list