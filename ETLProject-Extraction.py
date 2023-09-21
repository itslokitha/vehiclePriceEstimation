from urllib.request import urlopen
from bs4 import BeautifulSoup 

import datetime
import re

import pandas as pd
import numpy as np

def get_page_num(url):

    html = urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')
    try:
        page_info = bs.find('div',class_='showing').text
        page_num = page_info.split()[-2].replace(',','')
        page_num = int(int(page_num)/20)
    except:
        page_num = 1
        pass

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
        item_brand = bs_item.find(itemprop='brand').text
    except:
        item_brand =''
    
# Get model info    
    try:
        item_model = bs_item.find(itemprop='model').text
    except:
        item_model =''

# Get the model date
    try:
        item_date = bs_item.find(itemprop='vehicleModelDate').text
        item_date = int(item_date)
    except:
        item_date = 0

# Get list price :integer
    try:
        item_price = bs_item.find('span',itemprop='price').text
        item_price = int(item_price.replace('$','').replace(',','').replace('.',' ').split()[0])
    except:
        item_price = 0

# Get color
    try:
        item_color = bs_item.find(itemprop='color').text
    except:
        item_color = ''

# Get the configuration
    try:
        item_config = bs_item.find(itemprop='vehicleConfiguration').text
    except:
        item_config = ''

        
# Get the car condition
    try:
        item_condition = bs_item.find(itemprop='itemCondition').text
    except:
        item_condition = ''

        
# Get the body type
    try:
        item_bodytype = bs_item.find(itemprop='bodyType').text
    except:
        item_bodytype = ''

        
# Get the wheel configuration
    try:
        item_wheelConfig = bs_item.find(itemprop='driveWheelConfiguration').text
    except:
        item_wheelConfig = ''

# Get the transmission type
    try:
        item_transmission = bs_item.find(itemprop='vehicleTransmission').text
    except:
        item_transmission = ''

# Get the fuel type
    try:
        item_fueltype = bs_item.find(itemprop='fuelType').text
    except:
        item_fueltype = ''

# Get the mileage 
    try:
        item_mileage = bs_item.find(itemprop='mileageFromOdometer').text
        item_mileage = int(item_mileage.replace(',',''))
    except:
        item_mileage = 0
    
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

# Get vin number
    
    if 'vin=' in item_carfax_link:
        try:
            item_vin_number = item_carfax_link.replace('vin=',' ').split()[-1]
        except:
            item_vin_number = ''
            
            
# Get dealer's address        
    try:
        item_dealer_add = bs_item.find(itemprop='address').text
    except:
        item_dealer_add = ''
 

# Get car image link
    
    try:
        item_image = bs_item.find('img',itemprop='image')
        item_image_link = item_image.attrs['src']
    except: 
        item_image_link = ''
   
        

    
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

page_num

page_num = 3

all_info_list = []
itemlist = []
item_url = []

for page in range(1,page_num):
    page_url = 'https://www.kijiji.ca/b-city-of-halifax/'+'page+'+ str(page)+'/c27l1700321'
    html = urlopen(page_url)
    bs = BeautifulSoup(html, 'html.parser')
    for link in bs.find_all('a', href=re.compile('^(/v-cars-trucks/)((?!:).)*$')):
        print('Page:',page)
        if 'href' in link.attrs:
            item_url = base_url + link.attrs['href']
            if '?' not in item_url:
                try:
                    print(item_url)
                    itemlist = get_item_info(item_url)
                    #print(itemlist)
                    all_info_list.append(itemlist)
                    itemlist = []
                    
                except:
                    pass


df = pd.DataFrame(all_info_list)

df.head()

columns_name = ['brand','model','model_year','list_price','color','configration','condition','body_type',\
               'wheel_config','transmission','fuel_type','mileage','carfax_link','vin_number','image_link','dealer_address']

df.columns = columns_name


nan_value = float("NaN")
df.replace("", nan_value, inplace=True)
df.dropna(subset=['brand'],inplace=True)

df.head()

df.to_csv('kijiji_data_fullset.csv')

