import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

uber = pd.read_csv('uberPricesNew.csv')
uber["avg_estimate"] = (uber["high_estimate"] + uber["low_estimate"]) / 2
uber = uber[["place","dist","display_name","avg_estimate","time"]]
#print(uber.head())

lyft = pd.read_csv('lyftPricesNew.csv')
lyft["avg_estimate"] = (lyft["high_estimate"] + lyft["low_estimate"]) / 2
lyft= lyft[["place","dist","display_name","avg_estimate","time"]]
# lyft.head()

auber = pd.get_dummies(uber)
print(auber.columns)
Xuber = auber[['dist', 'place_Atlanta High Museum', 'place_Bartow',
       'place_Buckhead Bars', 'place_Butts', 'place_Centennial Park',
       'place_Cherokee', 'place_Clayton', 'place_Cobb', 'place_Coweta',
       'place_Dekalb', 'place_Douglas', 'place_Edgewood Bars',
       'place_Emory University', 'place_Fayette', 'place_Forsyth',
       'place_Fox Theater', 'place_Fulton', 'place_Georgia State University',
       'place_Gwinett', 'place_Hall', 'place_Hartsfield Jackson Airport',
       'place_Henry', 'place_Inman Park', 'place_Lenox Square Mall',
       'place_Mercedes Benz Stadium', 'place_Newton', 'place_Paulding',
       'place_Piedmont Park', 'place_Rockdale', 'place_Shops at Buckhead',
       'place_Six Flags', 'place_Spalding', 'place_Spelman College',
       'place_Statefarm Arena', 'place_Stone Mountain', 'place_SunTrust Park',
       'place_Virginia Highlands', 'place_Walton', 'place_Zoo Atlanta',
       'display_name_Black', 'display_name_Black SUV', 'display_name_Select',
       'display_name_UberPool', 'display_name_UberX', 'display_name_UberXL',
       'time_00:00', 'time_01:00', 'time_02:00', 'time_03:00', 'time_04:00',
       'time_05:00', 'time_06:00', 'time_07:00', 'time_08:00', 'time_09:00',
       'time_10:00', 'time_11:00', 'time_12:00', 'time_13:00', 'time_14:00',
       'time_15:00', 'time_16:00', 'time_17:00', 'time_18:00', 'time_19:00',
       'time_20:00', 'time_21:00', 'time_22:00', 'time_23:00']]

yuber = uber["avg_estimate"].values.reshape(-1, 1)

Xuber_train, Xuber_test, yuber_train, yuber_test = train_test_split(Xuber, yuber, random_state=42)

model_uber = LinearRegression()
model_uber.fit(Xuber_train, yuber_train)

regr_uber = RandomForestRegressor(max_depth=11, random_state=0, n_estimators=200)
regr_uber.fit(Xuber, yuber.ravel())

alyft = pd.get_dummies(lyft)
Xlyft = alyft[['dist', 'place_Atlanta High Museum', 'place_Bartow',
       'place_Buckhead Bars', 'place_Butts', 'place_Centennial Park',
       'place_Cherokee', 'place_Clayton', 'place_Cobb', 'place_Coweta',
       'place_Dekalb', 'place_Douglas', 'place_Edgewood Bars',
       'place_Emory University', 'place_Fayette', 'place_Forsyth',
       'place_Fox Theater', 'place_Fulton', 'place_Georgia State University',
       'place_Gwinett', 'place_Hall', 'place_Hartsfield Jackson Airport',
       'place_Henry', 'place_Inman Park', 'place_Lenox Square Mall',
       'place_Mercedes Benz Stadium', 'place_Newton', 'place_Paulding',
       'place_Piedmont Park', 'place_Rockdale', 'place_Shops at Buckhead',
       'place_Six Flags', 'place_Spalding', 'place_Spelman College',
       'place_Statefarm Arena', 'place_Stone Mountain', 'place_SunTrust Park',
       'place_Virginia Highlands', 'place_Walton', 'place_Zoo Atlanta',
       'display_name_Lux', 'display_name_Lux Black',
       'display_name_Lux Black XL', 'display_name_Lyft',
       'display_name_Lyft XL', 'display_name_Shared', 'time_00:00',
       'time_01:00', 'time_02:00', 'time_03:00', 'time_04:00', 'time_05:00',
       'time_06:00', 'time_07:00', 'time_08:00', 'time_09:00', 'time_10:00',
       'time_11:00', 'time_12:00', 'time_13:00', 'time_14:00', 'time_15:00',
       'time_16:00', 'time_17:00', 'time_18:00', 'time_19:00', 'time_20:00',
       'time_21:00', 'time_22:00', 'time_23:00']]

ylyft = lyft["avg_estimate"].values.reshape(-1, 1)

Xlyft_train, Xlyft_test, ylyft_train, ylyft_test = train_test_split(Xlyft, ylyft, random_state=42)

model_lyft = LinearRegression()
model_lyft.fit(Xlyft_train, ylyft_train)

regr_lyft = RandomForestRegressor(max_depth=11, random_state=0, n_estimators=200)
regr_lyft.fit(Xlyft, ylyft.ravel())

import pickle

#
# Create your model here (same as above)
#

# Save to file in the current working directory
uber_pkl_filename = "uber_model.pkl"  
with open(uber_pkl_filename, 'wb') as file:  
    pickle.dump(regr_uber, file)
    
# Save to file in the current working directory
lyft_pkl_filename = "lyft_model.pkl"  
with open(lyft_pkl_filename, 'wb') as file1:  
    pickle.dump(regr_lyft, file1)
    
    

