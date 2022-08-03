from tgtg import TgtgClient
import datetime
import sqlite3
import requests
from dotenv import load_dotenv
import os 

from urllib.parse import quote

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
conn = sqlite3.connect('TGTG.db',check_same_thread=False) 
c = conn.cursor()

def login(chat_id, email):
    client = TgtgClient(email=email)
    credentials = client.get_credentials()
    store_credentials(chat_id, credentials)
    return True

def store_credentials(chat_id, credentials):    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = 'insert into creds(chat_id,user_id,access_token,refresh_token,generated_at) VALUES(?, ?, ?, ?,?);'
    c.execute(sql, (chat_id,credentials['user_id'],credentials['access_token'],credentials['refresh_token'], current_time))
    conn.commit()

def remove_credentials(chat_id):
    removeItem = "DELETE FROM creds WHERE chat_id = ?"
    c.execute(removeItem, (chat_id,))
    conn.commit()
    return c.rowcount

def remove_sent_offers(chat_id):
    removeItem = "DELETE FROM sent_offers WHERE chat_id = ?"
    c.execute(removeItem, (chat_id,))
    conn.commit()
    return c.rowcount

def get_active_ids():
    sql = "SELECT chat_id FROM creds"
    c.execute(sql)
    result = c.fetchall()
    return [element[0] for element in result]


def request_offers(chat_id):
    sql = "SELECT user_id, access_token, refresh_token FROM creds WHERE chat_id=?"
    c.execute(sql, (chat_id,))
    result = c.fetchone()
    client = TgtgClient(access_token=result[1], 
                        refresh_token=result[2], 
                        user_id=result[0])
    items = client.get_items()
    offer_dict = get_offer_dict(items)
    return offer_dict

def get_offer_dict(items):
    fav={}
    for item in items:
        if int(item['items_available'])>0:
            fav[item['store']['store_id']] = {
                'store_name': item['display_name'],
                'address': item['store']['store_location']['address']['address_line'],
                'product_name': item['item']['name'],
                'quantity': item['items_available'],
                'pickup_interval': item['pickup_interval'],
                'price': 
                        {'old':float(item['item']['value_including_taxes']['minor_units'])/100, 
                        'new':float(item['item']['price_including_taxes']['minor_units'])/100,
                        'currency':item['item']['price_including_taxes']['code']},
                'rating':round(item['item']['average_overall_rating']['average_overall_rating'],1),
                'purchase_end': item['purchase_end']
            }
    return fav

def send_message(chat_id, message):
    SEND_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    requests.post(SEND_URL, json={'chat_id': chat_id, 'text': message}) 

def check_for_user(chat_id):
    offer_dict = request_offers(chat_id)
    to_send = determine_notifications(offer_dict, chat_id)
    for store_id in to_send:
        message = compose_message(offer_dict, store_id)
        send_message(chat_id, message)
        latest_pickup = extract_iso_date(offer_dict[store_id]['pickup_interval']['end'])
        insert_sent_offer(chat_id,store_id,latest_pickup)

def get_last_sent_offer_id():
    sql = "SELECT sent_offer_id FROM sent_offers"
    c.execute(sql)
    result = c.fetchall()
    if len(result)==0: return 0
    return max([int(element[0]) for element in result]) #maximum sent offer_id


def insert_sent_offer(chat_id,store_id, latest_pickup):
    new_sent_order_id = str(get_last_sent_offer_id()+1)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = 'insert into sent_offers(sent_offer_id,chat_id,store_id,sent_at_time,latest_pickup_time) VALUES(?, ?, ?, ?, ?);'
    c.execute(sql, (new_sent_order_id,chat_id,store_id,current_time,latest_pickup))
    conn.commit()

def determine_notifications(current_offers, chat_id,):
    sql = "SELECT store_id FROM sent_offers WHERE chat_id=?"
    c.execute(sql, (chat_id,))
    result = c.fetchall()
    sent_offers=set([element[0] for element in result])
    open_offers = set(current_offers.keys())
    eligible = open_offers.difference(sent_offers)
    return list(eligible)

def extract_date(time_string):
    parsed = datetime.datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%SZ")
    return parsed.strftime('%Y-%m-%d')

def extract_time(time_string):
    parsed = datetime.datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%SZ")
    return parsed.strftime('%H:%M')

def extract_iso_date(time_string):
    parsed = datetime.datetime.strptime(time_string, "%Y-%m-%dT%H:%M:%SZ")
    return parsed.strftime("%Y-%m-%d %H:%M:%S")

def construct_url(address):
    return quote(f'www.google.com/maps/place/{address}')
    
def compose_message(offer_dict,store_id):
    """    {'store_name': 'Albert Heijn to go - BOL.com (Magic Box)',
  'address': 'Papendorpseweg 100, 3528 BJ Utrecht, Nederland',
  'product_name': 'Magic Box',
  'quantity': 1,
  'pickup_interval': {'start': '2022-08-03T14:15:00Z',
   'end': '2022-08-03T14:45:00Z'},
  'price': {'old': 11.99, 'new': 3.99, 'currency': 'EUR'},
  'rating': 4.6} """
    order = offer_dict[store_id]
    return f"""{order['store_name']} (⭐{order['rating']}) NEW OFFER!
Offer 🛍️: {order['quantity']}X {order['product_name']}
Price 🤑: ~{"{:.2f}".format(order['price']['old'])}~ {"{:.2f}".format(order['price']['new'])} {order['price']['currency']}
Pickup 📆:  {extract_date(order['pickup_interval']['start'])} ➡️ ⏰ {extract_time(order['pickup_interval']['start'])} - {extract_time(order['pickup_interval']['end'])}
[NAVIGATE NOW]({construct_url(order['address'])})
"""



#ideas:
# maak een periodieke scraper om te kijken of een client nog actief is. If not active, verwijder entry.

#commands telegrambot
# login (send email, regex validatie) -> ook eentje voor confirmed (store credentials salted)
# resend email
# start_checking
# stop_checking