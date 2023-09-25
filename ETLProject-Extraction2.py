from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys

import pandas as pd

# Set up the WebDriver
chrome_path = "path_to_chromedriver.exe"  # Replace with the path to your ChromeDriver executable
selenium_service = ChromeService(executable_path=chrome_path)
browser = webdriver.Chrome(service=selenium_service)

def get_page_num(url):
    browser.get(url)
    page_info = browser.find_element(By.CLASS_NAME, 'showing').text
    page_num = int(page_info.split()[-2].replace(',', ''))
    page_num = (page_num // 20) + 1
    return page_num

def get_item_info(url):
    browser.get(url)
    item_info_list = []
    try:
        item_brand = browser.find_element(By.CSS_SELECTOR, '.sc-bdOgaJ.fVgBZP').text
    except:
        item_brand = ''
    # ... (rest of your code)
    return item_info_list

base_url = 'https://www.kijiji.ca'
init_url = 'https://www.kijiji.ca/b-city-of-halifax/l1700321'

page_num = get_page_num(init_url)

all_info_list = []

for page in range(1, page_num):
    page_url = f'https://www.kijiji.ca/b-city-of-halifax/page+{page}/c27l1700321'
    item_url = base_url + page_url
    try:
        itemlist = get_item_info(item_url)
        all_info_list.append(itemlist)
    except Exception as e:
        print(f"An error occurred: {e}")

df = pd.DataFrame(all_info_list)

# ... (rest of your code)
# test 2