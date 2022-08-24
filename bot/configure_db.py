import sqlite3

conn = sqlite3.connect('TGTG.db') 
c = conn.cursor()

c.execute('''
          CREATE TABLE IF NOT EXISTS creds
          ([chat_id] TEXT PRIMARY KEY, [user_id] TEXT, [access_token] TEXT, [refresh_token] TEXT, [generated_at] TEXT)
          ''')
          
c.execute('''
          CREATE TABLE IF NOT EXISTS sent_offers
          ([sent_offer_id] TEXT PRIMARY KEY, [chat_id] TEXT, [store_id] TEXT, [sent_at_time] TEXT, [latest_pickup_time] TEXT)
          ''')
                     
conn.commit()