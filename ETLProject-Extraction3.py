import requests
import time
import pandas as pd 
from bs4 import BeautifulSoup

# base URL for the Kijiji website
base_url = "https://www.kijiji.ca"

# URL for the first page
page_1_url = base_url + '/b-jewelry-watch/canada/watch/page-1/k0c133l0?rb=true' 

# use requests library to get respo
response = requests.get(page_1_url)

# use BS to parse the text of the HTML response
soup = BeautifulSoup(response.text, "lxml")

# find all of the relevant ads
ads = soup.find_all("div", attrs={"class": ["search-item", "regular-ad"]})

# removes marketing / third party ads
ads = [x for x in ads if ("cas-channel" not in x["class"]) & ("third-party" not in x["class"])]

# create a list to store all of the URLs from the 
ad_links = []
for ad in ads:
  # parse the link from the ad
  link = ad.find_all("a", {"class": "title"})
  # add the link to the list
  for l in link:
    ad_links.append(base_url + l["href"])

# create a dataframe to store our results
df = pd.DataFrame(columns=["title", "price", "description", "date_posted", 
                           "address", "url"])

for advert in (ad_links):
  # grab webpage information & transform with BS
  response = requests.get(advert)
  soup = BeautifulSoup(response.text, "lxml")

  # get ad title
  try:
      title = soup.find("h1").text
  except AttributeError:
      title = ""

  # get ad price
  try:
      price = soup.find("span", attrs={"itemprop": "price"}).text
  except AttributeError:
      price = ""

  # get date posted
  try:
      date_posted = soup.find("div", attrs={"itemprop": "datePosted"})['content']
  except (AttributeError, TypeError):
      date_posted = ""

  # get ad description
  try:
      description = soup.find("div", attrs={"itemprop": "description"}).text
  except AttributeError:
      description = ""

  # get the ad city
  try:
      address = soup.find("span", attrs={"itemprop": "address"}).text
  except AttributeError:
      address = ""

  # apend information to the dataframe
  df = df.append({
       "title": title,
       "price": price,
       "description": description,
       "date_posted": date_posted,
       "address": address, 
       "url": advert},
      ignore_index=True
  )

# save the final dataframe to a csv file
df.to_csv("kijiji_watch_data.csv")