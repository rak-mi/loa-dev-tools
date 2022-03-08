import pymongo
import datetime

def upload_market_to_db(market_data, db_url, date_time):
    client = pymongo.MongoClient(db_url)
    db=client.market_data

    for item in market_data:

        #get iso and epoch time for front end
        iso_date = datetime.datetime.strptime(date_time + "-0000", '%d%m%Y-%H%M%z')
        epoch_time = iso_date.timestamp()

        collection = db[item]
        data = {'_id': date_time, 'date': date_time, 'iso_date' : iso_date, 'epoch' : epoch_time, 'avg_price': market_data[item]['Average Price'], 'recent_price': market_data[item]['Recent Price'], 'lowest_price': market_data[item]['Lowest Price'], 'remaining_items': market_data[item]['Remaining Items']}
        result=collection.update_one({'_id': date_time}, {'$set': data}, upsert=True)

        if hasattr(result,'inserted_id'):
            print("Inserted the document", result.inserted_id)
        else:
            print("Updated " + str(item))

    client.close()

def upload_currency_to_db(currency_data, db_url, date_time):
    client = pymongo.MongoClient(db_url)
    db=client.mari_shop

    #get iso and epoch time for front end
    iso_date = datetime.datetime.strptime(date_time + "-0000", '%d%m%Y-%H%M%z')
    epoch_time = iso_date.timestamp()

    collection = db['currency_exchange']
    data = {'_id': date_time, 'date': date_time, 'iso_date' : iso_date, 'epoch' : epoch_time, 'exchange_rate': currency_data}
    result=collection.update_one({'_id': date_time}, {'$set': data}, upsert=True)

    if hasattr(result,'inserted_id'):
        print("Inserted the document", result.inserted_id)
    else:
            print("Updated " + str(currency_data))

    client.close()

#Get currency exchange price from db
def get_currency_exchange_from_db(db_url):
    client = pymongo.MongoClient(db_url)
    db = client.mari_shop

    collection = db['currency_exchange']
    results = collection.find().sort('date', -1).limit(1)
    for result in results:
        return (result)

    client.close()

#Get auction house prices from db
def get_ah_price_from_db(db_url, name):
    client = pymongo.MongoClient(db_url)
    db = client.market_data

    collection = db[name]
    results = collection.find().sort('date', -1).limit(1)
    for result in results:
        price = result['lowest_price']
        date = result['date']
        return (price, date)

    client.close()
