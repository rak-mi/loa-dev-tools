from locale import currency
from pprint import PrettyPrinter
from screen_scrape import scrape, auto_utils
from db_handle import db
import json
import configparser
import datetime
import glob

#Open up config file and get the db_url
config = configparser.ConfigParser()
config.read('conf.ini')
db_url = config['mongo-db']['url']

#list of screenshots to process

mari_shop_list = ['mari_shop_honing', 'mari_shop_tradeskill']

enhancement_file_list = glob.glob("screenshots\\market\\*.png")

#process each market screenshot and upload to db
index = 0
for enhancement_file in enhancement_file_list:
    enhancement = (enhancement_file[-36:-18])
    date_time = (enhancement_file[-17:-4])
    
    response = scrape.get_aution_house_prices(enhancement_file, enhancement, date_time)
    db.upload_market_to_db(response, db_url, date_time)
    index += 1

mari_file_list = glob.glob("screenshots\\mari\\*.png")
#process each mari screenshot and upload to db
for mari_shop_file in mari_file_list:

    date_time = (mari_shop_file[-17:-4])
    mari_shop = (mari_shop_file[-26:-18])
    mari_slot = auto_utils.convert_time_into_mari_time(date_time)
    response = scrape.get_mari_prices(mari_shop_file, mari_shop, mari_slot)
    db.upload_mari_to_db(response, db_url, mari_slot)

#process currency exchange and upload to db
currency_file_list = glob.glob("screenshots\\currency\\*.png")
for currency_file in currency_file_list:
    date_time = (currency_file[-17:-4])
    avg_currency = int(scrape.get_currency_exchange(currency_file, 'currency_exchange'))
    db.upload_currency_to_db(avg_currency, db_url, date_time)