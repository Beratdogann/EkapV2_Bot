import sqlite3
import pandas as pd # type: ignore

def oku(veritabani_adi, tablo_adi, limit=10):
    with sqlite3.connect(veritabani_adi) as conn:
        df = pd.read_sql_query(f"SELECT * FROM {tablo_adi} LIMIT {limit}", conn)
    return df
