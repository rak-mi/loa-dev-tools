
from PIL import Image
import pytesseract
import cv2
import numpy as np
import json

def prepare_data_summary(data):
    summary_data = {}
    for item, value in data.items():
        summary_data[item] = {}
        summary_data[item] = value['Recent Price']
    return summary_data

def get_aution_house_prices(screenshot_path, descriptor, file_date, w, h):

    #import resoltion json from json_data
    with open('json_data/resolution.json', 'r') as outfile:
        resolution = json.load(outfile)
    
    resolutions = w + " x " + h
    res_index = resolution[resolutions]

    img = cv2.imread(screenshot_path)
    item_list = img[res_index['market_y']['start']:res_index['market_y']['end'], res_index['item_x']['start']:res_index['item_x']['end']]
    avg_list = img[res_index['market_y']['start']:res_index['market_y']['end'], res_index['avg_x']['start']:res_index['avg_x']['end']]
    recent_list = img[res_index['market_y']['start']:res_index['market_y']['end'], res_index['recent_x']['start']:res_index['recent_x']['end']]
    lowest_list = img[res_index['market_y']['start']:res_index['market_y']['end'],  res_index['lowest_x']['start']:res_index['lowest_x']['end']]

    response = {}

    items = get_items(item_list)
    #avg = get_price_list(avg_list, 3, 2)
    recent = get_price_list(recent_list, 3, 2)
    low = get_price_list(lowest_list, 3, 2)
    
    index = 0
    for item in items:
        if recent[index] == None or low[index] == None:
            index += 1
            continue
        #print('adding item: ', item)
        #print('avarage price: ', avg[index])
        #print('recent price:', recent[index])
        #print('lowest price:', low[index])
        response[item] = {}
        #response[item]['Average Price'] = avg[index]
        response[item]['Recent Price'] = recent[index]
        response[item]['Lowest Price'] = low[index]
        response[item]['Remaining Items'] = 100 #hard coded for now
        index += 1
    
    return response


def get_currency_exchange(screenshot_path, descriptor, w, h):
    img = cv2.imread(screenshot_path)

    #import resoltion json from json_data
    with open('json_data/resolution.json', 'r') as outfile:
        resolution = json.load(outfile)

    resolutions = w + " x " + h
    res_index = resolution[resolutions]

    price_list = img[res_index['currency_y']['start'] : res_index['currency_y']['end'], res_index['currency_x']['start']:res_index['currency_x']['end']]
    prices = get_price_list(price_list, 4, 2)
    avg_price = sum(prices) / len(prices)
    return (avg_price)

def get_items(item_list):
    #image magic to manipulate the image to be easier for tesseract to read
    inv_item_list = cv2.bitwise_not(item_list)
    gray_item_list = cv2.cvtColor(inv_item_list, cv2.COLOR_BGR2GRAY)
    #gray_item_list = inv_item_list

    #cv2.imshow('dilate', gray_item_list)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
    #get the readable list of items
    market_items = pytesseract.image_to_string(gray_item_list , config="--oem 3 --psm 4", lang = 'eng')

    market_list = market_items.split('\n')
    item_list = []
    index = -1
    #slight hardcoding on the items
    for item in market_list:
        print('item name?', item)
        if item == '\x0c' or item.isspace() or item == '':
            pass
        elif item == '[Sold in bundles of 10 units]':
            item_list[index] = item_list[index] + ' (10)'
        else:
            index += 1
            if item == 'ar\'s Breath':
                item = 'Star\'s Breath'
            item_list.append(item)

    print('item_list:', item_list)
    return item_list

def get_price_list(price_list, dilate1, dilate2):
    # Stretching the image a bit to improve ocr results
    img = price_list
    width = int(img.shape[1] + 35)
    height = int(img.shape[0])
    dim = (width, height)

    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    #image magic to manipulate the image to be easier for tesseract to read
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((dilate1, dilate2), 'uint8')
    dilate_img = cv2.dilate(gray, kernel, iterations=1)
    reverse = cv2.bitwise_not(dilate_img)

    #cv2.imshow('dilate', reverse)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    #get the average price of the item
    item_list = pytesseract.image_to_data(reverse , config="--oem 3 --psm 6", lang = 'eng', output_type=pytesseract.Output.DICT)

    price_item_list = []
    #some hardcoding on false positives
    for item in item_list['text']:
        #print(item)
        if item != '':
            if item == 'i' or item == 'I':
                price_item_list.append(1.0)
            elif item == '1a':
                price_item_list.append(12.0)      
            elif item == '5B':
                price_item_list.append(58.0)
            else:
                try:
                    price_item_list.append(float(item.replace(',', '')))
                except Exception as e:
                    price_item_list.append(None)

    #print(price_item_list)
    return price_item_list
