import pymongo

def upload_market_to_db(market_data, db_url, date_time):

    client = pymongo.MongoClient(db_url)

    db=client.market_data
    # Issue the serverStatus command and print the results
    serverStatusResult=db.command("serverStatus")

    for item in market_data:
        #Step 3: Insert business object directly into MongoDB via insert_one
        collection = db[item]
        data = {'_id': date_time, 'date': date_time, 'avg_price': market_data[item]['Average Price'], 'recent_price': market_data[item]['Recent Price'], 'lowest_price': market_data[item]['Lowest Price'], 'remaining_items': market_data[item]['Remaining Items']}

        result=collection.update_one({'_id': date_time}, {'$set': data}, upsert=True)
            #Step 4: Print to the console the ObjectID of the new document
        if hasattr(result,'inserted_id'):
            print("Inserted the document", result.inserted_id)
        else:
            print("Updated " + str(item))

    client.close()

def upload_mari_to_db(mari_shop, db_url, id):
    client = pymongo.MongoClient(db_url)

    db=client.mari_shop

    # Issue the serverStatus command and print the results
    serverStatusResult=db.command("serverStatus")

    for item in mari_shop:
        collection = db['enhancement']
        items = list(mari_shop[item].keys())
        data = {'_id': item, 'item_1_name': items[0],
                'item_1_price': mari_shop[item][items[0]]['price'],
                'item_1_ammount': mari_shop[item][items[0]]['ammount'],
                'item_2_name': items[1],
                'item_2_price': mari_shop[item][items[1]]['price'],
                'item_2_ammount': mari_shop[item][items[1]]['ammount'],
                'item_3_name': items[2],
                'item_3_price': mari_shop[item][items[2]]['price'],
                'item_3_ammount': mari_shop[item][items[2]]['ammount'],
                'item_4_name': items[3],
                'item_4_price': mari_shop[item][items[3]]['price'],
                'item_4_ammount': mari_shop[item][items[3]]['ammount'],
                'item_5_name': items[4],
                'item_5_price': mari_shop[item][items[4]]['price'],
                'item_5_ammount': mari_shop[item][items[4]]['ammount'],
                'item_6_name': items[5],
                'item_6_price': mari_shop[item][items[5]]['price'],
                'item_6_ammount': mari_shop[item][items[5]]['ammount']}

        result=collection.update_one({'_id': item}, {'$set': data}, upsert=True)
            #Step 4: Print to the console the ObjectID of the new document

        if hasattr(result,'inserted_id'):
            print("Inserted the document", result.inserted_id)
        else:
            print("Updated " + str(item))
        
    client.close()

def upload_currency_to_db(currency_data, db_url, date_time):
    client = pymongo.MongoClient(db_url)

    db=client.mari_shop

    # Issue the serverStatus command and print the results
    serverStatusResult=db.command("serverStatus")

    collection = db['currency_exchange']
    data = {'_id': date_time, 'date': date_time, 'exchange_rate': currency_data}

    result=collection.update_one({'_id': date_time}, {'$set': data}, upsert=True)
        #Step 4: Print to the console the ObjectID of the new document
    if hasattr(result,'inserted_id'):
        print("Inserted the document", result.inserted_id)
    else:
            print("Updated " + str(currency_data))

    client.close()

def get_mari_prices_from_db(db_url, id):
    client = pymongo.MongoClient(db_url)
    db = client.mari_shop
    collection = db['enhancement']
    result = collection.find_one({'_id': id})
    return result

def get_currency_exchange_from_db(db_url, id):
    client = pymongo.MongoClient(db_url)
    db = client.mari_shop
    collection = db['currency_exchange']
    result = collection.find_one({'_id': id})
    return result

def get_ah_price_from_db(db_url, name, id):
    client = pymongo.MongoClient(db_url)
    db = client.market_data
    collection = db[name]
    result = collection.find_one({'_id': id})
    price = result['lowest_price']
    return float(price)