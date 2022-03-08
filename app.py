from screen_scrape import scrape
from db_handle import mongdb, firebasedb
import configparser
import glob
import argparse


#Open up config file and get the db_url
config = configparser.ConfigParser()
config.read('conf.ini')
db_url = config['mongo-db']['url']

#Arguments to choose mode/width/height
parser = argparse.ArgumentParser(description='args')
parser.add_argument('-mode', '-M', metavar='mode',  type=str, help='market mode or currency exchange mode')
parser.add_argument('-width', '-W',  metavar='width', type=str, help='width of screen')
parser.add_argument('-height','-H',  metavar='height',type=str, help='height of screen')
parser.add_argument('-db',  metavar='database',type=str, help='Database type')
args = parser.parse_args()

if args.db != 'mongodb' and args.db != 'firebase':
    print('Please choose a valid database(mongodb or firebase)')
    print(args.db)
    exit()

#list of screenshots to process
enhancement_file_list = glob.glob("screenshots\\market\\*.png")

#get information from market
if args.mode == 'market':
    #process each market screenshot and upload to db
    for enhancement_file in enhancement_file_list:
        try:
            enhancement = (enhancement_file[-36:-18])
            date_time = (enhancement_file[-17:-4])   
            response = scrape.get_aution_house_prices(enhancement_file, enhancement, date_time, args.width, args.height)
            if args.db == 'mongodb':
                mongdb.upload_market_to_db(response, db_url, date_time)
            if args.db == 'firebase':
                firebasedb.upload_market_to_db(response, 'honing_items', date_time)

        except Exception as e:
            print("Error processing screenshot: ", enhancement_file)
            print(e)
            continue

#get information from currency exchange
elif args.mode == 'currency':
    #process currency exchange and upload to db
    currency_file_list = glob.glob("screenshots\\currency\\*.png")
    for currency_file in currency_file_list:
        try:
            date_time = (currency_file[-17:-4])
            avg_currency = int(scrape.get_currency_exchange(currency_file, 'currency_exchange'))
            if args.db == 'mongodb':
                mongdb.upload_currency_to_db(avg_currency, db_url, date_time)
            if args.db == 'firebase':
                firebasedb.upload_currency_to_db(avg_currency, 'currency_exchange', date_time)
            
        except Exception as e:
            print("Error processing screenshot: ", currency_file)
            print(e)
            continue

#unknown mode
else:
    print("Invalid mode")
    exit()