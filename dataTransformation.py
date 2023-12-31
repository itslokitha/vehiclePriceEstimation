# Name: Lokitha Nilaweera (157736)
# Project: Capstone Project
# Department: Computer Science
# School: Acadia University
# Title: Vehicle Price Predictor - NS
# Supervisor: Dr. Danny Silver
# Program Title: dataTransformation.py

import os
import pandas as pd

csv_directory = 'datasheets'

master_df = pd.DataFrame()

for filename in os.listdir(csv_directory):
    if filename.endswith('.csv'):

        file_path = os.path.join(csv_directory, filename)
        df = pd.read_csv(file_path)
        
        df_cleaned = df.drop_duplicates(subset=['model_year', 'brand', 'model', 'mileage', 'color', 'list_price'], keep='last')
        df_cleaned = df_cleaned[df_cleaned['list_price'] != 0]
        
        master_df = pd.concat([master_df, df_cleaned], ignore_index=True)

master_df.to_csv('master_data.csv', index=False)