## SQLiteLite Module
### 概述
> 此模組提供了一個簡單的介面來操作 SQLite 資料庫，包含資料表的創建、資料插入、查詢、索引建立等功能。
> A module that makes it easier for users to use sqlite3.

### 安裝
請確保已安裝 `Python 3.11` 以上，以及 `termcolor` 套件。你可以使用以下命令安裝 termcolor：

```ps
pip install termcolor
```

### 使用方法
#### 初始化
首先，導入並初始化 SQLITE 類別，指定資料庫路徑：
```python
from SQLiteLite import SQLITE

db = SQLITE("your_database.db")
創建資料表
使用 creat_table 方法創建資料表：

python
Copy code
table_name = "your_table"
table_columns = {
    "column1": "INTEGER",
    "column2": "TEXT",
    "column3": "TEXT"
}

db.creat_table(table_name, table_columns)
```

#### 插入資料
使用 insert_data 方法插入資料：
```python
table_data = {
    "column1": 1,
    "column2": "Example",
    "column3": "Data"
}

db.insert_data(table_name, table_data)
```

#### 查詢資料
使用 get_datas 方法查詢資料：
```python
results = db.get_datas("your_table", "column_name", "value")
print(results)
```

使用 get_datas_fuzzy 方法進行模糊查詢：
```python
fuzzy_results = db.get_datas_fuzzy("your_table", "column_name", "partial_value")
print(fuzzy_results)
```

使用 get_total_data_count 方法取得所有資料數量：
```python
total_count = db.get_total_data_count("your_table")
print(total_count
```

#### 檢查資料表或欄位是否存在
使用 is_exist_table_name 方法檢查資料表是否存在：
```python
exists = db.is_exist_table_name("your_table")
print(exists)
```

使用 is_exist_column_name 方法檢查欄位是否存在：
```python
column_exists = db.is_exist_column_name("your_table", "column_name")
print(column_exists)
```

#### 建立索引
使用 creat_index 方法在資料表上建立索引：
```python
db.creat_index("your_table", "column_name")
```

#### 確認資料是否已存在
使用 is_exist_data 方法確認資料是否已存在：
```python
data_exists = db.is_exist_data("your_table", "column_name", "value")
print(data_exists)
```

#### 優化資料庫
使用 vacuum 方法優化資料庫：
```python
db.vacuum()
```

#### 獲取資料表的欄位資訊
使用 get_columns_info 方法獲取資料表的欄位資訊：
```python
columns_info = db.get_columns_info("your_table")
print(columns_info)
```

#### 範例程式碼
以下是一個完整的範例程式碼，展示了如何使用此模組：
```python
 # 初始化資料庫
 s = SQLITE("Game.db")
 # 創建資料表
 s.creat_table("RPG", {"job": "INT", "Name": "TEXT", "items": "TEXT"})
 # 插入資料
 s.insert_data("RPG", {"job": 111, "Name": "Alice", "items": "Potion, Arrow"})
 s.insert_data("RPG", {"job": 999, "Name": "Bob", "items": "Bread, Potion"})
 s.insert_data("RPG", {"job": 999, "Name": "Clair", "items": "Candy, MageBook"})
 s.insert_data("RPG", {"job": 000, "Name": "David", "items": "Potion"})
 # 建立索引
 s.creat_index("RPG", "job")
 # 獲取資料表列表
 print(f"tables: {s.get_tables()}\n")
 # 獲取 RPG 資料表的欄位列表
 print(f"RPG column: {s.get_columns('RPG')}\n")
 # 查詢 job 為 111 的資料
 print(f'Job is 111 result:\n{s.get_datas("RPG", "job", "111")}\n')
 # 模糊查詢 items 中包含 "Potion" 的資料
 print(f'Items include Potion result:\n{s.get_datas_fuzzy("RPG", "items", "Potion")}\n')
 # 確認 Name 為 Bob 的資料是否存在
 print(f'Is Bob in Name: {s.is_exist_data("RPG", "Name", "Bob")}\n')
 # 獲取 RPG 資料表中的總資料數量
 print(f'Total data count: {s.get_total_data_count("RPG")}\n')
 # 獲取 RPG 資料表的欄位資訊
 print(f'RPG column info: {s.get_columns_info("RPG")}')
 # 優化資料庫
 s.vacuum()
```

### 作者
> steveh8758@gmail.com
> [name=Steven, Hsin]