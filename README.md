# Django-SideProject

### 專案架構:
```
Django_sideproject/
│
├── myapp/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── static
│       └── myapp
│           └── js
│               └── index.js   #主要JS
│   └── templates
│       └── myapp
│           └── index.html     #首頁顯示
│
├── myproject/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── db.sqlite3
├── manage.py     # Django主程式
├── get_data.py   # 第一次獲取資料並放到SQLite3 程式
├── test.py       # 測試功能程式
├── manage.py     # 每日自動抓取公開資料並放到Mongodb程式


```
---

### 框架:

#### 前端框架:  
**Bootstrap 5**  
**Datatables**  
#### 後端框架:  
**Python - Django**  
#### 資料庫:  
**SQLite3**  
#### 反向代理:  
**Apache2**  

---

### 待改善部分:

1. UID 欄位應該不能被編輯
2. 編輯應該需要另外一個頁面或是按鈕，再行編輯
3. 使用者登入應該透過DB, 而非Django 內建Create_User
4. 搜尋功能應該可以搜尋所有關鍵字
5. Show Info 資訊應該也需要可以被編輯, 或是需要讓他表格再大一點
6. 排版問題

---

### 網頁使用說明:

1. 登入首頁之後, 會直接顯示所有資料庫資料, 並可以透過Datatables 進行簡易排序功能
2. 使用者未登入時, 可以使用搜尋功能
3. 可以使用登入按鈕進行登入註冊, 會提醒最低限度的帳號/密碼長度
4. 註冊並登入後, 即可使用更新與刪除功能
5. 點選兩下表格可以進行編輯, 編輯完成後按下更新按鈕則就可以更新完成(目前UID可編輯, 尚待排除Bug)
6. 勾選前方框格, 選取後可進行資料刪除
7. 右側Show Details 會顯示詳細的Show Info 資訊


### 自動化撈取公開資料說明:

1. 使用Linux 內建 service , 將python file 作為一個服務啟動
2. 每日凌晨1點會呼叫 公開資訊API , 並放入Database
3. 呼叫完後會同時放在一個api_responses.txt 作為備份

---

### 說明SQL 與 NO-SQL 差異 與 說明兩者使用場景

#### SQL資料庫
1. 資料模型： SQL資料庫，也稱為關聯式資料庫，使用嚴格的表格結構來組織資料。 這些表格之間透過關係（例如外鍵）相互連接

2. 查詢語言： 使用結構化查詢語言（SQL），SELECT * FROM Table ... 等
3. 一致性模型： 大多數遵循ACID（原子性、一致性、隔離性、持久性）原則
4. 可伸縮性： 適合垂直伸縮（增強單一伺服器的能力）
5. 應用場景： 適用於需要複雜查詢、事務完整性和嚴格資料模型的場景，如金融服務、庫存管理...等
#### NoSQL資料庫
1. 資料模型： NoSQL資料庫支援多種資料模型，包括鍵值對、文件、寬列和圖形資料庫，不強制使用固定的表結構
2. 查詢語言： 例如Mongodb 使用 JSON格式進行搜尋, 沒有固定形式,  
             **example:** records = db_EMS.E_dReg_Daily.find({'status': 0})
3. 可伸縮性： 設計為易於水平伸縮，透過增加更多伺服器來提高效能和容量(Mongodb PSS、Slice架構)
4. 應用場景： 資料格式可能會一直調整，如電商、論壇留言資訊...等

### 何謂資料庫正規化

1. 其目的是為了降低資料的「重覆性」避免「更新異常」的情況發生。

2. 將整個資料表中重複性的資料剔除剔除，，否則在關聯表中會造成造成新增、異常、修改異常的狀況發生。
3. 一般而言，正規化的精神就是讓資料庫中最重複的欄位資料減到最少，並且能快速的找到資料，以提高關聯性資料庫的效能。

---

