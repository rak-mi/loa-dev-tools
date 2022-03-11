import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import json
import time

cred = credentials.Certificate("secret.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

def upload_market_to_db(market_data, da_type, date_time):

    for item in market_data:
        #get iso and epoch time for front end
        iso_date = datetime.datetime.strptime(date_time + "-0000", '%d%m%Y-%H%M%z')
        epoch_time = iso_date.timestamp()

        data = {u'date': date_time, u'iso_date' : iso_date, u'epoch' : epoch_time, u'avg_price': market_data[item]['Average Price'], u'recent_price': market_data[item]['Recent Price'], u'lowest_price': market_data[item]['Lowest Price'], u'remaining_items': market_data[item]['Remaining Items']}
        db.collection(u'market').document(da_type).collection(str(item)).document(str(date_time)).set(data)
        print("Updated " + str(item))

def upload_currency_to_db(currency_data, db_url, date_time):

    #get iso and epoch time for front end
    iso_date = datetime.datetime.strptime(date_time + "-0000", '%d%m%Y-%H%M%z')
    epoch_time = iso_date.timestamp()

    data = {'date': date_time, 'iso_date' : iso_date, 'epoch' : epoch_time, 'exchange_rate': currency_data}
    db.collection(u'market').document(u'currency_exchange').collection('Prices').document(str(date_time)).set(data)
    print("Updated " + str('currency_exchange'))

def make_scrape_log():
    t = int(time.time())
    data = {u'timestamp': firestore.SERVER_TIMESTAMP, u'status': 'SUCCESS'}
    db.collection(u'scrape_logs').document(str(t)).set(data)
    print('Logged', data)

def make_market_summary(data):
    t = int(time.time())
    db.collection(u'market_summary').document(str(t)).set(data)