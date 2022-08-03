# nu meerdere schedulers maken.
# TGTG bot moet altijd runnen

# eerste schedulers loopt over de sql db heen, en checkt offers en sends notifications
# de andere scheduler gaat eens per half uur: kijk of de key nog werkt per user.
# de andere scheduler eens per uur: kijk of huidige tijd oude tijd exceeded is. 
import datetime
from datetime import datetime

from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
import sqlite3

import TGTG_framework

conn = sqlite3.connect('TGTG.db',check_same_thread=False) 
c = conn.cursor()
print('SEARCHING')

scheduler = BlockingScheduler()
@scheduler.scheduled_job(IntervalTrigger(seconds=60))
def search_for_offers():
    print('SEARCHING')
    active_list = TGTG_framework.get_active_ids()
    for chat_id in active_list:
        TGTG_framework.check_for_user(chat_id)

@scheduler.scheduled_job(IntervalTrigger(hours=6))
def remove_expired_deals():
    sql = "DELETE FROM sent_offers WHERE latest_pickup_time < ?"
    c.execute(sql,(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
    conn.commit()
    


scheduler.start()

# print('SEARCHING')
# active_list = get_active_ids()
# for chat_id in active_list:
#     TGTG_framework.check_for_user(chat_id)