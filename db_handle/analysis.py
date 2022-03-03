import db
import json


def get_mari_price_analysis(db_url,mari_id,price_id):
    mari_prices = db.get_mari_prices_from_db(db_url, mari_id)
    currency_exchange = db.get_currency_exchange_from_db(db_url, price_id)

    #open translate .json and load into dictionary
    with open('json_data/translate-mari-to-auction-house.json') as json_file:
        translate = json.load(json_file)

    blu_to_gold_exchange_rate = float(currency_exchange['exchange_rate']) / 95.0

    for x in range(1,7):
        mari_gold_price = mari_prices['item_' + str(x) + '_price'] * blu_to_gold_exchange_rate / mari_prices['item_' + str(x) + '_ammount']
        ah_val = translate[mari_prices['item_' + str(x) + '_name']]
        if '10' in ah_val:
            ah_gold_price = db.get_ah_price_from_db(db_url, ah_val, price_id) / 10.0
        else:
            ah_gold_price = db.get_ah_price_from_db(db_url, ah_val, price_id)
        print(mari_prices['item_' + str(x) + '_name'])
        print('\t Analysis -> {:0.2f}%'.format((float(ah_gold_price) / float(mari_gold_price) * 100.0)))
        print('\t Mari Gold Cost per Item-> {:0.2f}'.format((mari_gold_price)))
        print('\t Auction House Gold Cost per Item -> {:0.2f}'.format((ah_gold_price)))
