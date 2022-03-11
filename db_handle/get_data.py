import firebase_admin
from firebase_admin import credentials, firestore
import datetime

cred = credentials.Certificate("secret.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

#Get currency exchange price from db
def get_currency_exchange_from_db():
    collection = db.collection(u'cash_shop').document('currency_exchange').collection('gold_prices')

    result = collection.order_by(u'date', direction=firestore.Query.DESCENDING).limit(1).get()[0]
    if result.exists:
        return(result.to_dict())
    else:
        return None

#Get auction house prices from db
def get_ah_price_from_db(da_type, item):
    collection = db.collection(u'market').document(da_type).collection(str(item))

    result = collection.order_by(u'date', direction=firestore.Query.DESCENDING).limit(1).get()[0]
    if result.exists:
        return(result.to_dict())
    else:
        return None