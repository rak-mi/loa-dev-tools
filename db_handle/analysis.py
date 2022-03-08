from db_handle import db
import json
import pymongo

def get_mari_prices_from_db(db_url, id):
    client = pymongo.MongoClient(db_url)
    db = client.mari_shop
    collection = db['enhancement']
    result = collection.find_one({'_id': id})
    return result

def get_currency_exchange_from_db(db_url):
    client = pymongo.MongoClient(db_url)
    db = client.mari_shop
    collection = db['currency_exchange']
    results = collection.find().sort('date', -1).limit(1)
    for result in results:
        return (result)

def get_ah_price_from_db(db_url, name):
    client = pymongo.MongoClient(db_url)
    db = client.market_data
    collection = db[name]
    results = collection.find().sort('date', -1).limit(1)
    for result in results:
        price = result['lowest_price']
        date = result['date']
        return (price, date)


def get_mari_price_analysis(db_url,mari_id):
    out_str = ''
    mari_prices = get_mari_prices_from_db(db_url, mari_id)
    if mari_prices is None:
        return ("No mari prices found")

    currency_exchange = get_currency_exchange_from_db(db_url)

    #open translate .json and load into dictionary
    with open('json_data/translate-mari-to-auction-house.json') as json_file:
        translate = json.load(json_file)

    blu_to_gold_exchange_rate = float(currency_exchange['exchange_rate']) / 95.0

    for x in range(1,7):
        mari_gold_price = mari_prices['item_' + str(x) + '_price'] * blu_to_gold_exchange_rate / mari_prices['item_' + str(x) + '_ammount']
        ah_val = translate[mari_prices['item_' + str(x) + '_name']]
        try:
            if '10' in ah_val:
                ah_gold_price = get_ah_price_from_db(db_url, ah_val) / 10.0
            else:
                ah_gold_price = get_ah_price_from_db(db_url, ah_val)

            out_str += (mari_prices['item_' + str(x) + '_name'])
            out_str += ('\t Analysis -> {:0.2f}%'.format((float(ah_gold_price) / float(mari_gold_price) * 100.0)))
            out_str += ('\t Mari Gold Cost per Item-> {:0.2f}'.format((mari_gold_price)))
            out_str += ('\t Auction House Gold Cost per Item -> {:0.2f}'.format((ah_gold_price)))

        except:
            out_str += (mari_prices['item_' + str(x) + '_name'])
            out_str += ('\t Failed to find price')

    return(out_str)

