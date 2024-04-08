# ===========================================================================

# import requests

# # 要訪問的網址
# url = "https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJ&category=1"

# # 發送 GET 請求
# response = requests.get(url)

# # 檢查請求是否成功
# if response.status_code == 200:
#     data = response.json()
#     print(data)
# else:
#     print("請求失敗，狀態碼：", response.status_code)

# ===========================================================================
# # # 獲取數據
# import sqlite3
# import requests

# response = requests.get("https://cloud.culture.tw/frontsite/trans/SearchShowAction.do?method=doFindTypeJ&category=1")
# data = response.json()

# conn = sqlite3.connect('events.db')
# c = conn.cursor()

# # Events
# c.execute('''
# CREATE TABLE IF NOT EXISTS Events (
#     UID TEXT PRIMARY KEY,
#     title TEXT,
#     category TEXT,
#     descriptionFilterHtml TEXT,
#     imageUrl TEXT,
#     webSales TEXT,
#     sourceWebPromote TEXT,
#     comment TEXT,
#     editModifyDate TEXT,
#     sourceWebName TEXT,
#     startDate TEXT,
#     endDate TEXT,
#     hitRate INTEGER
# )
# ''')

# #  ShowInfo 表
# c.execute('''
# CREATE TABLE IF NOT EXISTS ShowInfo (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     event_uid TEXT,
#     time TEXT,
#     location_id INTEGER,
#     onSales TEXT,
#     price TEXT,
#     endTime TEXT,
#     FOREIGN KEY(event_uid) REFERENCES Events(UID),
#     FOREIGN KEY(location_id) REFERENCES Locations(id)
# )
# ''')

# #  Locations 表
# c.execute('''
# CREATE TABLE IF NOT EXISTS Locations (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     location TEXT UNIQUE,
#     locationName TEXT,
#     latitude TEXT,
#     longitude TEXT
# )
# ''')

# c.execute('''
# CREATE TABLE IF NOT EXISTS MasterUnits (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     event_uid TEXT,
#     unit_name TEXT,
#     FOREIGN KEY(event_uid) REFERENCES Events(UID)
# )
# ''')


# # 插入数据
# for item in data:
#     # 插入到 Events 表
#     c.execute('INSERT OR IGNORE INTO Events (UID, title, category, descriptionFilterHtml, imageUrl, webSales, sourceWebPromote, comment, editModifyDate, sourceWebName, startDate, endDate, hitRate) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
#               (item['UID'], item['title'], item['category'], item.get('descriptionFilterHtml', ''), item.get('imageUrl', ''), item.get('webSales', ''), item.get('sourceWebPromote', ''), item.get('comment', ''), item.get('editModifyDate', ''), item.get('sourceWebName', ''), item['startDate'], item['endDate'], item.get('hitRate', 0)))

#     # 插入到 ShowInfo 和 Locations 表
#     for show in item['showInfo']:
#         # 檢查 location 是否已存在
#         c.execute('SELECT id FROM Locations WHERE location = ?', (show['location'],))
#         location_id = c.fetchone()

#         if not location_id:
#             c.execute('INSERT INTO Locations (location, locationName, latitude, longitude) VALUES (?, ?, ?, ?)', (show['location'], show.get('locationName', ''), show.get('latitude', ''), show.get('longitude', '')))
#             location_id = c.lastrowid
#         else:
#             location_id = location_id[0]

#         # 插入 ShowInfo
#         c.execute('INSERT INTO ShowInfo (event_uid, time, location_id, onSales, price, endTime) VALUES (?, ?, ?, ?, ?, ?)', 
#                   (item['UID'], show['time'], location_id, show.get('onSales', ''), show.get('price', ''), show.get('endTime', '')))
        
#     if 'masterUnit' in item and item['masterUnit']:
#         for unit in item['masterUnit']:
#             c.execute('INSERT INTO MasterUnits (event_uid, unit_name) VALUES (?, ?)', (item['UID'], unit))
#     else:
#         # 如果 masterUnit 为空或不存在，插入一个带有占位符的记录
#         c.execute('INSERT INTO MasterUnits (event_uid, unit_name) VALUES (?, ?)', (item['UID'], "N/A"))

# conn.commit()

# conn.close()


# ===========================================================================
# 連接到 SQLite3 數據庫
# conn = sqlite3.connect('events.db')
# c = conn.cursor()

# # 查詢 Events 表中的所有數據
# c.execute('SELECT * FROM ShowInfo ORDER BY Time DESC;')
# events = c.fetchall()

# print("ShowInfo :")
# for event in events:
#     print(event)

# # 查詢特定條件的數據，例如查找特定 UID 的活動
# target_uid = '你的目標UID'
# c.execute('SELECT * FROM Events WHERE UID = ?', (target_uid,))
# specific_event = c.fetchone()

# if specific_event:
#     print("\nSpecific event with UID", target_uid, ":", specific_event)
# else:
#     print("\nNo event found with UID", target_uid)

# # 關閉連接
# conn.close()

from django.contrib.auth.models import User

user = User.objects.get(username='test')
user.set_password('test123')
user.save()