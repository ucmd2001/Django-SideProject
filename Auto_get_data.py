#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from apscheduler.schedulers.background import BackgroundScheduler
import time
import requests
import pymongo
import os
import json

conn_local = pymongo.MongoClient('mongodb://127.0.0.1:27017/', serverSelectionTimeoutMS=1000)
db_local = conn_local["API_data"]


def write_log(message):
    with open("/var/www/Django_sideproject/api_responses.txt", "a") as log_file:
        log_file.write(json.dumps(message) + "\n")  

def Auto_get_data():
    # # 要訪問的網址
    url = "https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJ&category=1"

    # 發送 GET 請求
    response = requests.get(url)

    # 檢查請求是否成功
    if response.status_code == 200:
        data = response.json()
        #print(data)
        # 多放一筆資料當備援
        write_log(data)
        # 放資料到Database
        db_local.Music_Performance_info.insert_many(data)
    else:
        print("請求失敗，狀態碼：", response.status_code)

#Auto_get_data()

if __name__ == "__main__":
    print("---------------------------------------------------------")
    print("Press Ctrl+{0} to exit".format("Break" if os.name == "nt" else "C"))
    print("---------------------------------------------------------")
    scheduler = BackgroundScheduler()
    scheduler.start()

    # Auto_get_data
    scheduler.add_job(Auto_get_data, 'cron', hour=1, minute=0)

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Exit The Job!")
