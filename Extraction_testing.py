# Name: Lokitha Nilaweera (157736)
# Project: Capstone Project
# Department: Computer Science
# School: Acadia University
# Title: Vehicle Price Predictor - NS
# Supervisor: Dr. Danny Silver
# Program Title: extraction.py

from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import re
import os
import pandas as pd
import numpy as np

def get_page_num(url):
    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')
    try:
        page_info = bs.find('div', class_='showing').text
        page_num = page_info.split()[-2].replace(',', '')
        page_num = int(int(page_num) / 20)
    except Exception as e:
        print(f"Error in get_page_num: {e}")
        page_num = 1
    return page_num

def get_item_info(url):
    item_info_list = []
    item_brand = ''
    item_model = ''
    item_date = ''
    item_price = ''
    item_color = ''
    item_config = ''
    item_condition = ''
    item_bodytype = ''
    item_wheelConfig = ''
    item_transmission = ''
    item_fueltype = ''
    item_mileage = ''
    item_carfax_link = ''
    item_vin_number = ''
    item_image_link = ''
    item_dealer_add = ''
    html = urlopen(url)
    bs_item = BeautifulSoup(html, 'html.parser')

# Get brand info
    try: 
        make = bs_item.find_all('span', class_='sc-dNsVcS cjFKdZ')
        item_brand = make[1].text
        print (item_brand)
    except:
        item_brand =''
        print ("Brand not found")

# Get model info    
    try:
        model = bs_item.find_all('span', class_='sc-dNsVcS cjFKdZ')
        item_model = model[2].text
        print (item_model)
    except:
        item_model =''
        print ("Model not found")

# Get the model year
    try:
        year = bs_item.find_all('span', class_='sc-dNsVcS cjFKdZ')
        item_date = year[0].text
        print (item_date)
    except:
        item_date = 0
        print ("Year not found")

# Get list price :integer
    try:
        item_price = bs_item.find('span',itemprop='price').text
        item_price = int(item_price.replace('$','').replace(',','').replace('.',' ').split()[0])
        print (item_price)
    except:
        item_price = 0
        print ("Price not found")

# Get color
    try:
        color = bs_item.find_all('span', class_='sc-dNsVcS cjFKdZ')
        item_color = color[4].text
        print (item_color)
    except:
        item_color = ''
        print ("Color not found")

# Get the configuration (Error due to site change)
    # try:
    #     item_config = bs_item.find(itemprop='vehicleConfiguration').text
    # except:
    #     item_config = ''
    #     print ("Vehicle configuration not found")
        
# Get the car condition
    try:
        condition = bs_item.find_all('span', class_='sc-lnPyaJ dkyjZe')
        item_condition = condition[0].text
        print (item_condition)
    except:
        item_condition = ''
        print ("Vehicle condition not found")
        
# Get the body type
    try:
        bodytype = bs_item.find_all('span', class_='sc-dNsVcS cjFKdZ')
        item_bodytype = bodytype[5].text
        print (item_bodytype)
    except:
        item_bodytype = ''
        print ("Bodytype not found")
        
# Get the wheel configuration
    try:
        drivetrain = bs_item.find_all('span', class_='sc-dNsVcS cjFKdZ')
        item_wheelConfig = drivetrain[6].text
        print (item_wheelConfig)
    except:
        item_wheelConfig = ''
        print ("Drivetrain not found")

# Get the transmission type
    try:
        transmission = bs_item.find_all('span', class_='sc-dNsVcS cjFKdZ')
        item_transmission = transmission[7].text
        print (item_transmission)
    except:
        item_transmission = ''
        print ("Transmission not found")

# Get the fuel type
    try:
        fueltype = bs_item.find_all('span', class_='sc-dNsVcS cjFKdZ')
        item_fueltype = fueltype[8].text
        print (item_fueltype)
    except:
        item_fueltype = ''
        print ("Fueltype not found")

# Get the mileage 
    try:
        mileage = bs_item.find_all('span', class_='sc-lnPyaJ dkyjZe')
        item_mileage = mileage[1].text
        item_mileage = int(item_mileage.replace(',',''))
        print (item_mileage)

    except:
        item_mileage = 0
        print ("Mileage not found")
    
# Car Accident Report link
    item_carfax = bs_item.find('a', href=re.compile('^(https://reports.carproof.com)((?!:).)*$'))
    try:
        item_carfax_link = item_carfax.attrs['href']

    except:
        item_carfax = bs_item.find('a', href=re.compile('^(https://www.carproof.com)((?!:).)*$'))
        try: 
            item_carfax_link = item_carfax.attrs['href']
        except:
            item_carfax_link = ''
            print ("Accident report link is not found")

# Get vin number
    try:
        vin = bs_item.find_all('span', class_='sc-dNsVcS cjFKdZ')
        item_vin_number = vin[9].text
        print (item_vin_number)

    except:
        item_vin_number = ''
        print ("VIN number not found")  
            
# Get dealer's address        
    try:

        address = bs_item.find('a', class_='link-3970392289 link__default-1151936189 location-582645639')
        item_dealer_add = address.text
        print (item_dealer_add)

    except:
        item_dealer_add = ''
        print ("Address not found")
 
# Get car image link

    try:
        item_image = bs_item.find('img', class_='image-3484370594 heroImageBackground-2776220296')
        item_image_link = item_image['src']
        print (item_image_link)
    except: 
        item_image_link = ''
        print ("Car image not found")
        

    item_info_list.append(item_brand)
    item_info_list.append(item_model)
    item_info_list.append(item_date)
    item_info_list.append(item_price)
    item_info_list.append(item_color)
    item_info_list.append(item_config)
    item_info_list.append(item_condition)
    item_info_list.append(item_bodytype)
    item_info_list.append(item_wheelConfig)
    item_info_list.append(item_transmission)
    item_info_list.append(item_fueltype)
    item_info_list.append(item_mileage)
    item_info_list.append(item_carfax_link)
    item_info_list.append(item_vin_number)
    item_info_list.append(item_image_link)
    item_info_list.append(item_dealer_add)

    return item_info_list

base_url = 'https://www.kijiji.ca'
init_url = 'https://www.kijiji.ca/b-city-of-halifax/l1700321'
page_num = get_page_num(init_url)

all_info_list = []
for page in range(1, page_num + 400):
    page_url = f'https://www.kijiji.ca/b-city-of-halifax/page-{page}/c27l1700321'
    html = urlopen(page_url)
    bs = BeautifulSoup(html, 'html.parser')
    for link in bs.find_all('a', href=re.compile('^(/v-cars-trucks/)((?!:).)*$')):
        print('Page:', page)
        if 'href' in link.attrs:
            item_url = base_url + link.attrs['href']
            if '?' not in item_url:
                try:
                    print(item_url)
                    itemlist = get_item_info(item_url)
                    print(itemlist)  # Used this line for Debugging purposes to see which data are extracted and which are not in the console
                    all_info_list.append(itemlist)
                except Exception as e:
                    print(f"Error in loop: {e}")
                    pass

# Check if all_info_list is populated
print(all_info_list)

# Create DataFrame
columns_name = ['brand', 'model', 'model_year', 'list_price', 'color', 'configuration', 'condition', 'body_type',
                'wheel_config', 'transmission', 'fuel_type', 'mileage', 'carfax_link', 'vin_number', 'image_link', 'dealer_address']
df = pd.DataFrame(all_info_list, columns=columns_name) if all_info_list else pd.DataFrame(columns=columns_name)

# Replace empty strings with NaN and drop rows where 'brand' is NaN
nan_value = float("NaN")
df.replace("", nan_value, inplace=True)
df.dropna(subset=['brand'], inplace=True)

print(df)

today_date = datetime.date.today().strftime('%Y-%m-%d')
outputDirectory = 'datasheets'
if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory)
file_name = f'kijiji_data_{today_date}.csv' # Creates the datasheet with the specific date
file_path = os.path.join(outputDirectory, file_name)

df.to_csv(file_path, index=False)