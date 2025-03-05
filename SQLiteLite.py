# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 01:34:46 2024

@author: Steven, Hsin
@email: steveh8758@gmail.com
"""

import sqlite3
import os
import inspect
from termcolor import colored

class SQLiteConnection:

    def __init__(self, db_path:str):
        self.db_path = db_path
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print("ROLLBACKED!")
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

class SQLITE:

    def __init__(self, db_path:str):
        self.db_path = db_path

    def execute(self, query:str, *args) -> list | dict:
        with SQLiteConnection(self.db_path) as con:
            cursor = con.cursor()
            try:
                cursor.execute(query, *args)
            except sqlite3.IntegrityError:
                con.rollback()
            except Exception as e:
                con.rollback()
                print(f"An unexpected error occurred: {e}")
            rt = cursor.fetchall()
        return rt

    def create_table(self, table_name:str, table_columns: dict[str, str]) -> None:
        exe_str = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        for k,v in table_columns.items():
            exe_str +=  f"\n\t{k} {v},"
        exe_str = f"{exe_str.rstrip(',')})"
        # print(exe_str)
        self.execute(exe_str)

    def get_tables(self) -> list:
        exe_str = "SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'"
        exe_res = self.execute(exe_str)
        return [row[0] for row in exe_res] if exe_res != [] else []

    def get_columns(self, table_name: str) -> list:
        exe_str = f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        result = self.execute(exe_str)
        if result:
            create_statement = result[0][0]
            start = create_statement.index("(") + 1
            end = create_statement.rindex(")")
            columns = create_statement[start:end].split(",")
            columns = [col.strip().split()[0] for col in columns]
            return columns
        else:
            return None

    def is_exist_table_name(self, table_name: str) -> bool:
        # if any(table_name == i for i in self.get_tables()):
        #     return True
        return table_name in self.get_tables()

    def is_exist_column_name(self, table_name: str, column_name: str) -> bool:
        # if any(column_name == i for i in self.get_columns(table_name)):
        #     return True
        return column_name in self.get_columns(table_name)

    def create_index(self, table_name: str, column_name: str) -> None:
        if not self.is_exist_table_name(table_name):
            raise KeyError(f"Can't find `{table_name}` in database.")
        if not self.is_exist_column_name(table_name, column_name):
            raise KeyError(f"Can't find `{column_name}` in `{table_name}` .")
        index_name = f"idx_{table_name}_{column_name}"
        exe_str = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} ({column_name})"
        self.execute(exe_str)

    def insert_data(self, table_name:str, table_data: dict[str, any]) -> None:
        if not self.is_exist_table_name(table_name):
            raise KeyError(f"Can't find `{table_name}` in database.")
        database_keys = set(self.get_columns(table_name))
        table_data_keys = set(table_data.keys())
        if table_data_keys != database_keys:
            diff = list(database_keys.symmetric_difference(table_data_keys) & table_data_keys)
            raise KeyError(f"The key of the inserted data must be the same as the key of the database. Different keys: {diff}")
        columns = ', '.join(table_data.keys())
        placeholders = ', '.join('?' * len(table_data))
        values = list(table_data.values())
        exe_str = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
        self.execute(exe_str, values)

    def vacuum(self) -> None:
        self.execute('VACUUM')

    def is_exist_data(self, table_name: str, column_name: str, data: str) -> bool:
        if len(self.get_datas(table_name, column_name, data)) > 0:
            print(colored(f"{os.path.basename(inspect.stack()[0].filename)} -> '{data}' Already in DB.", "yellow"))
            return True
        return False

    def get_datas(self, table_name: str, column_name: str, data: str) -> list[tuple]:
        exe_str = f"SELECT * FROM {table_name} WHERE {column_name} = ?"
        return self.execute(exe_str, (data,))

    def get_datas_fuzzy(self, table_name: str, column_name: str, data: str) -> list[tuple]:
        exe_str = f"SELECT * FROM {table_name} WHERE {column_name} LIKE ?"
        return self.execute(exe_str, (f'%{data}%',))

    def get_total_data_count(self, table_name: str) -> int:
        if not self.is_exist_table_name(table_name):
            raise KeyError(f"Can't find `{table_name}` in database.")
        exe_str = f"SELECT COUNT(*) FROM {table_name}"
        result = self.execute(exe_str)
        return int(result[0][0]) if result else 0

    def get_columns_info(self, table_name: str) -> list[tuple]:
        if not self.is_exist_table_name(table_name):
            raise KeyError(f"Can't find `{table_name}` in database.")
        exe_str = f"PRAGMA table_info('{table_name}')"
        return self.execute(exe_str)

if __name__ == '__main__':
    # 初始化資料庫
    s = SQLITE("Game.db")
    # 創建資料表
    s.create_table("RPG", {"job": "INT", "Name": "TEXT", "items": "TEXT"})
    # 插入資料
    s.insert_data("RPG", {"job": 111, "Name": "Alice", "items": "Potion, Arrow"})
    s.insert_data("RPG", {"job": 999, "Name": "Bob", "items": "Bread, Potion"})
    s.insert_data("RPG", {"job": 999, "Name": "Clair", "items": "Candy, MageBook"})
    s.insert_data("RPG", {"job": 000, "Name": "David", "items": "Potion"})
    # 建立索引
    s.create_index("RPG", "job")
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
