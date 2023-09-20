import pandas as pd
import numpy as np

car_df = pd.read_csv('kijiji_data_fullset.csv')

car_df.head()

car_df['brand'].value_counts()

car_df = car_df.replace('na','0')

# model_year type to int

car_df['model_year'] = pd.to_numeric(car_df['model_year'])


# price type to int
i= 0
for item_price in car_df['list_price']:
    if item_price == '0':
       item_price = int(item_price)
       car_df.loc[i,'list_price'] = item_price
    else:
      # item_price =item_price.replace('$','').replace(',','').replace('.',' ').split()[0]
       car_df.loc[i,'list_price'] = item_price
       item_price=int(item_price)
    i+=1


# mileage type to int
i = 0

for odo_mileage in car_df['mileage']:
    if odo_mileage == '0':
         car_df.loc[i,'mileage'] = 0
    else:
        try:
            car_df.loc[i,'mileage'] = int(odo_mileage.replace(',',''))
        except:
            pass
    i+=1

car_df.head()

import matplotlib.pyplot as plt

# Plot

make_count = car_df.groupby('model_year')['brand'].count()

make_count_frame = make_count.to_frame()

make_count_frame.rename(columns={'brand':'total numbers'},inplace=True)
make_count_frame.head()


fig = make_count_frame.plot(kind = 'bar',figsize=(14, 10), title = 'Total car sales on Kijiji website in Halifax Area').get_figure()
fig.savefig('kijiji_car_count.png')

brand_count = car_df.groupby('brand')['model_year'].count()

brand_count_df = brand_count.to_frame()

brand_count_df.rename(columns={'model_year':'brand total numbers'},inplace=True)

brand_count_df = brand_count_df.sort_values(by=['brand total numbers'])
fig = brand_count_df.plot(kind = 'bar',figsize=(14, 10), title = 'Brand Numbers on Kijiji website in Halifax area').get_figure()
fig.savefig('kijiji_brand_count.png')

df= car_df
model_type = pd.DataFrame()
for b in list(df["brand"].unique()):
    for v in list(df["body_type"].unique()):
        z = df[(df["brand"] == b) & (df["body_type"] == v)]["list_price"].mean()
        model_type = model_type.append(pd.DataFrame({'brand':b , 'body_type':v , 'avgPrice':z}, index=[0]))
model_type = model_type.reset_index()
del model_type["index"]
model_type["avgPrice"].fillna(0,inplace=True)
model_type["avgPrice"].isnull().value_counts()
model_type["avgPrice"] = model_type["avgPrice"].astype(int)
model_type.head(5)

import seaborn as sns
# HeatMap tp show average prices of vehicles by brand and type together
tri = model_type.pivot("brand","body_type", "avgPrice")
fig, ax = plt.subplots(figsize=(15,20))
sns_plot = sns.heatmap(tri,linewidths=1,cmap="YlGnBu",annot=True, ax=ax, fmt="d").get_figure()
ax.set_title("Average price of vehicles by vehicle type and brand",fontdict={'size':20})
ax.xaxis.set_label_text("Type Of Vehicle",fontdict= {'size':20})
ax.yaxis.set_label_text("Brand",fontdict= {'size':20})
sns_plot.savefig('kijiji_type_price.png')
plt.show()

df= car_df
mile_price = pd.DataFrame()
for b in list(df["brand"].unique()):
    for v in list(df["body_type"].unique()):
        z = df[(df["brand"] == b) & (df["body_type"] == v)]["mileage"].mean()
        mile_price = mile_price.append(pd.DataFrame({'brand':b , 'body_type':v , 'avgMileage':z}, index=[0]))
mile_price = mile_price.reset_index()
del mile_price["index"]
mile_price["avgMileage"].fillna(0,inplace=True)
mile_price["avgMileage"].isnull().value_counts()
mile_price["avgMileage"] = mile_price["avgMileage"].astype(int)
mile_price.head(5)

tri = mile_price.pivot("brand","body_type", "avgMileage")
fig, ax = plt.subplots(figsize=(15,20))
sns_plot = sns.heatmap(tri,linewidths=1,cmap="YlOrRd",annot=True, ax=ax, fmt="d").get_figure()
ax.set_title("Average mileage of vehicles by vehicle type and brand",fontdict={'size':20})
ax.xaxis.set_label_text("Type Of Vehicle",fontdict= {'size':20})
ax.yaxis.set_label_text("Brand",fontdict= {'size':20})
sns_plot.savefig('kijiji_type_mileage.png')
plt.show()

avg_mile = mile_price.groupby('brand')['avgMileage'].mean()
avg_mile_df = avg_mile.to_frame()
avg_mile_df = avg_mile_df.sort_values(by=['avgMileage'])

fig = avg_mile_df.plot(kind='bar',figsize=(14, 10), title = 'Average Mileages based on Brands on Kijiji website').get_figure()
fig.savefig('kijiji_average_mileage.png')


brand_avg_price = model_type

brand_avg_price = brand_avg_price.groupby('brand')['avgPrice'].mean()
brand_avg_price_df = brand_avg_price.to_frame()
brand_avg_price_df = brand_avg_price_df.sort_values(by=['avgPrice'])

fig = brand_avg_price_df.plot(kind='bar',figsize=(14, 10), title = 'Average Price based on Brands on Kijiji website').get_figure()
fig.savefig('kijiji_average_price.png')
