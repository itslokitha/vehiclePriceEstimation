import pandas as pd
import csv
import pymysql
pymysql.install_as_MySQLdb()
import config
from sqlalchemy import create_engine

conn = create_engine('mysql://root:jinbanruo2jinheyu@127.0.0.1/favorite_db')
kijiji_full_df = pd.read_csv('kijiji_car.csv')
kijiji_full_df.to_sql('kijiji_origin', con=conn)
kijiji_full_df = pd.read_csv('kijiji_data_fullset.csv')
kijiji_full_df.to_sql('kijiji_ful', con=conn)

autolist_df = pd.read_csv('data/auto_trader_mpgdata.csv')

autolist_df.to_sql('autolist_data', con=conn)
