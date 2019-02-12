import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

import pickle


uber_dist = pd.read_csv('uberPricesNew.csv')
uber_dist = uber_dist[["place","dist","time"]]
uber_dist.head()
uber_dist = pd.get_dummies(uber_dist)
Xdu = uber_dist[['place_Atlanta High Museum', 'place_Bartow',
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
       'time_00:00', 'time_01:00', 'time_02:00', 'time_03:00', 'time_04:00',
       'time_05:00', 'time_06:00', 'time_07:00', 'time_08:00', 'time_09:00',
       'time_10:00', 'time_11:00', 'time_12:00', 'time_13:00', 'time_14:00',
       'time_15:00', 'time_16:00', 'time_17:00', 'time_18:00', 'time_19:00',
       'time_20:00', 'time_21:00', 'time_22:00', 'time_23:00']]
ydu = uber_dist["dist"].values.reshape(-1, 1)
print(Xdu.shape, ydu.shape)

Xdu_train, Xdu_test, ydu_train, ydu_test = train_test_split(Xdu, ydu, random_state=42)
modeldu = LinearRegression()
modeldu.fit(Xdu_train, ydu_train)

uberd_pkl_filename = "uberd_modeldu.pkl"  
with open(uberd_pkl_filename, 'wb') as file:  
    pickle.dump(modeldu, file)


lyft_dist = pd.read_csv('lyftPricesNew.csv')
lyft_dist= lyft_dist[["place","dist","time"]]
lyft_dist.head()
lyft_dist = pd.get_dummies(lyft_dist)
Xdl = lyft_dist[['place_Atlanta High Museum', 'place_Bartow',
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
       'time_00:00', 'time_01:00', 'time_02:00', 'time_03:00', 'time_04:00',
       'time_05:00', 'time_06:00', 'time_07:00', 'time_08:00', 'time_09:00',
       'time_10:00', 'time_11:00', 'time_12:00', 'time_13:00', 'time_14:00',
       'time_15:00', 'time_16:00', 'time_17:00', 'time_18:00', 'time_19:00',
       'time_20:00', 'time_21:00', 'time_22:00', 'time_23:00']]
ydl = lyft_dist["dist"].values.reshape(-1, 1)
# print(Xdl.shape, ydl.shape)

Xdl_train, Xdl_test, ydl_train, ydl_test = train_test_split(Xdl, ydl, random_state=42)

modeldl = LinearRegression()
modeldl.fit(Xdl_train, ydl_train)

lyftd_pkl_filename = "lyftd_modeldl.pkl"  
with open(lyftd_pkl_filename, 'wb') as file1:  
    pickle.dump(modeldl, file1)