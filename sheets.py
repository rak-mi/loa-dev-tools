import gspread
from oauth2client.service_account import ServiceAccountCredentials
from db_handle import mongdb
import json
import configparser
import datetime

#Open up config file and get the db_url
config = configparser.ConfigParser()
config.read('conf.ini')
db_url = config['mongo-db']['url']

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('sheets-api.json', scope)

#load json postions from json file
with open('json_data\sheet-positions.json') as json_file:
    sheet_positions = json.load(json_file)

# authorize the clientsheet 
client = gspread.authorize(creds)

#open the sheet
sheet = client.open('Azena - Lost Ark - Gold vs Crystals')
sheet_instance = sheet.get_worksheet(0)

#get currency price
currency_price = mongdb.get_currency_exchange_from_db(db_url)
sheet_instance.update_cell(18,14, str(int(currency_price['exchange_rate'])))

epoch = currency_price['epoch']
local_time_new_date = datetime.datetime.fromtimestamp(epoch)
new_date = local_time_new_date.strftime("%d%m%Y-%H%M")
date_time = new_date.split('-')


datea = date_time[0][2:4] + '/' + date_time[0][:2] + '/' + date_time[0][4:]
time = date_time[1][:2] + ':' + date_time[1][2:]
print(str(currency_price['exchange_rate']) + ' -> ' + datea + '-' + time)

#update last update date for currency exchange rate
sheet_instance.update_cell(30,12, str(datea))
sheet_instance.update_cell(30,13, str(time))


#update each item with the latest lowest praice
date_time_list = []
for tier in sheet_positions:
    for item_name in sheet_positions[tier]:
        #get the item price and update sheet
        result = mongdb.get_ah_price_from_db(db_url, item_name)
        sheet_location = sheet_positions[tier][item_name]
        sheet_instance.update_cell(sheet_location,4, str(int(result['lowest_price'])))

        #conver to local time
        epoch = result['epoch']
        local_time_new_date = datetime.datetime.fromtimestamp(epoch)
        new_date = local_time_new_date.strftime("%d%m%Y-%H%M")
        date_time = new_date.split('-')

        #log information
        datea = date_time[0][2:4] + '/' + date_time[0][:2] + '/' + date_time[0][4:]
        time = date_time[1][:2] + ':' + date_time[1][2:]
        print(item_name + ' : ' + str(int(result['lowest_price'])) + ' -> ' + datea + '-' + time)

        #add to list to sort later
        date_time_list.append(new_date)


#get oldest date out of the list of updated items
sorted_dates = sorted(date_time_list)
date_time = sorted_dates[0].split('-')
datea = date_time[0][2:4] + '/' + date_time[0][:2] + '/' + date_time[0][4:]
time = date_time[1][:2] + ':' + date_time[1][2:]

#update the last updated date with oldest date of the list
sheet_instance.update_cell(30,4, str(datea))
sheet_instance.update_cell(30,6, str(time))
