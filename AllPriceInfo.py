import os
import json
# from shapely.geometry import Polygon
from numpy import random
# from shapely.geometry import Point
import pandas as pd

# libraries for UBER API
from uber_rides.session import Session
from uber_rides.client import UberRidesClient

# libraries for take the capture date
import time
from datetime import datetime, timedelta
# libraries for capture data each 4 min
import threading
import requests
import json


from uber_rides.session import Session
ubersession = Session(server_token="TZ9aAN7GMzp49djfXoMil2HJ7XxCs0Zwo8EWXd88")

from uber_rides.client import UberRidesClient
client = UberRidesClient(ubersession)


from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()
# Define our lyftPrices table
class LyftPricesNew(Base):
    __tablename__ = 'lyftPricesNew'
    id = Column(Integer, primary_key=True)
    place = Column(String)
    lat = Column(Integer)
    lon = Column(Integer)
    dist = Column(Integer)
    display_name = Column(String)
    duration = Column(Integer)
    estimate = Column(String)
    high_estimate = Column(Integer)
    low_estimate = Column(Integer)
    autotime = Column(String)
    time = Column(String)
    day = Column(String)
    company = Column(String)
    
    
    
engine = create_engine('sqlite:///LyftPricesNew.sqlite')
Base.metadata.create_all(engine)


Base1 = declarative_base()
# Define our uberPrices table
class UberPricesNew(Base1):
    __tablename__ = 'uberPricesNew'
    id = Column(Integer, primary_key=True)
    place = Column(String)
    lat = Column(Integer)
    lon = Column(Integer)
    dist = Column(Integer)
    display_name = Column(String)
    duration = Column(Integer)
    estimate = Column(String)
    high_estimate = Column(Integer)
    low_estimate = Column(Integer)
    autotime = Column(String)
    time = Column(String)
    day = Column(String)
    company = Column(String)
    
engine1 = create_engine('sqlite:///UberPricesNew.sqlite')
Base1.metadata.create_all(engine1)


places = [
  { "name": "Centennial Park",
  "location": [33.7603474,-84.3957012]},
  { "name": "Buckhead Bars",
  "location": [33.8439849,-84.3789694]},
  { "name": "Inman Park",
  "location": [33.7613676,-84.3623401]},
  { "name": "Stone Mountain",
  "location": [33.8053189,-84.1477255]},
  { "name": "Six Flags",
  "location": [33.7706408,-84.5537186]},
  { "name": "Statefarm Arena",
 "location": [33.7572891,-84.3963244]},
 { "name": "Zoo Atlanta",
 "location": [33.7327032,-84.3846396]},
 { "name": "Atlanta High Museum",
 "location": [33.7900632,-84.3877407]},
 { "name": "Fox Theater",
 "location": [33.7724591,-84.3879697]},
 { "name": "Virginia Highlands",
 "location": [33.7795027,-84.3757217]},
 { "name": "Shops at Buckhead",
 "location": [33.838031,-84.3821468]},
 { "name": "Emory University",
 "location": [33.7925239,-84.3261929]},
 { "name": "Georgia State University",
 "location": [33.7530724,-84.3874759]},
 { "name": "Spelman College",
 "location": [33.7463641,-84.4144874]},
 { "name": "Edgewood Bars",
 "location": [33.7544814,-84.3745674]},
  {"name": "Hartsfield Jackson Airport",
  "location": [33.6407282,-84.4277001]},
   {"name":"SunTrust Park",
   "location":[33.8908211,-84.4678309]},
   {"name":"Mercedes Benz Stadium",
   "location":[33.7554483,-84.400855]},
   {"name":"Lenox Square Mall",
    "location":[33.8462925,-84.3621419]},
   {"name":"Piedmont Park",
   "location":[33.7850856,-84.373803]},
   {"name":"Hall",
   "location":[34.3063924,-83.9791498]},
   {"name":"Forsyth",
   "location":[33.0369172,-83.9534595]},
   {"name":"Cherokee",
   "location":[34.2431482,-84.5984968]},
   {"name":"Bartow",
   "location":[34.2443826,-84.9857677]},
   {"name":"Paulding",
   "location":[33.928889,-85.0268574]},
   {"name":"Douglas",
   "location":[33.6899886,-84.8846799]},
   {"name":"Coweta",
   "location":[33.3516087,-84.8962848]},
   {"name":"Fayette",
   "location":[33.4039244,-84.6445094]},
   {"name":"Spalding",
   "location":[33.2658534,-84.4391148]},
   {"name":"Butts",
   "location":[33.3126177,-84.105586]},
   {"name":"Newton",
   "location":[33.5559292,-84.0049789]},
   {"name":"Walton",
   "location":[33.7635877,-83.8840724]},
   {"name":"Gwinett",
   "location":[33.960546,-84.178047]},
   {"name":"Fulton",
   "location":[33.8446039,-84.7543888]},
   {"name":"Cobb",
   "location":[33.9126755,-84.6972663]},
   {"name":"Clayton",
   "location":[33.5008779,-84.491477]},
   {"name":"Henry",
   "location":[33.4727666,-84.278534]},
   {"name":"Rockdale",
   "location":[33.6561613,-84.1887709]},
   {"name":"Dekalb",
   "location":[33.7929946,-84.327053]}]
   



def collect_lyft_data():
    lyft_total_estimates = []
    estimates = {}
    #Global Learning Center GA TECH: 33.7762° N, 84.3895° W

    for place in places:
        estimates = {}

        url="https://api.lyft.com/v1/cost?start_lat=33.7762&start_lng=-84.3895&end_lat=" +str(place["location"][0])+ "&end_lng="+str(place["location"][1])
        # requests.get(url).json()

        estimate = requests.get(url).json()["cost_estimates"]
        #print(estimate)
        #estimate10
        estimates["place"] = place["name"]
        estimates["geometry"] = place["location"]
        autotimeinit = datetime.now()
        autotime = autotimeinit.strftime('%H:%M')
        estimates["autotime"] = autotime
        autohour = autotimeinit.strftime('%H')
        autohour = autohour + ":00"
        estimates["time"] = autohour
        autoday = autotimeinit.strftime('%A')
        estimates["day"] = autoday
        estimates["value"] = estimate
        # last_hour_date_time = datetime.now() - timedelta(hours = 1)
        # list_datetime_capture.append(last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S'))
        lyft_total_estimates.append(estimates)
    # lyft_total_estimates
    # print(len(lyft_total_estimates))



    # Create our database engine
    engine = create_engine('sqlite:///LyftPricesNew.sqlite')

    # Base.metadata.create_all(engine)
    # The ORM’s “handle” to the database is the Session.
    
    session = Session(engine)

    # Note that adding to the session does not update the table. It queues up those queries.
    for values in lyft_total_estimates:
        for value in values["value"]:
            session.add(LyftPricesNew(place=values["place"], lat=values["geometry"][0], lon=values["geometry"][1], 
                                   dist=value["estimated_distance_miles"], display_name = value["display_name"], 
                                   duration = value["estimated_duration_seconds"], 
                                    estimate = str(value["estimated_cost_cents_min"]//100) + " - " +str(value["estimated_cost_cents_max"]//100),
                                   high_estimate = value["estimated_cost_cents_max"]//100, 
                                    low_estimate = value["estimated_cost_cents_min"]//100,
                                   autotime=values["autotime"], time=values["time"],
                                      day=values["day"], company="Lyft"
                                  ))

    # commit() flushes whatever remaining changes remain to the database, and commits the transaction.
    # print("lyft done")
    session.commit()
    
    
    
def collect_uber_data():
    total_estimates = []
    estimates = {}
    #Global Learning Center GA TECH: 33.7762° N, 84.3895° W

    for place in places:
        estimates = {}
        response = client.get_price_estimates(
            start_latitude=33.7762,
            start_longitude=-84.3895,
            end_latitude=place["location"][0],
            end_longitude=place["location"][1]
        )

        estimate = response.json.get('prices')
        #print(estimate)
        #estimate10
        estimates["place"] = place["name"]
        estimates["geometry"] = place["location"]
        autotimeinit = datetime.now()
        autotime = autotimeinit.strftime('%H:%M')
        estimates["autotime"] = autotime
        autohour = autotimeinit.strftime('%H')
        autohour = autohour + ":00"
        estimates["time"] = autohour
        estimates["value"] = estimate
        autoday = autotimeinit.strftime('%A')
        estimates["day"] = autoday
        estimates["value"] = estimate
        # last_hour_date_time = datetime.now() - timedelta(hours = 1)
        # list_datetime_capture.append(last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S'))
        total_estimates.append(estimates)
    
    # print(len(total_estimates))
    
    engine1 = create_engine('sqlite:///UberPricesNew.sqlite')
    session1 = Session(engine1)
    
    # Note that adding to the session does not update the table. It queues up those queries.
    for values in total_estimates:
        for value in values["value"]:
            session1.add(UberPricesNew(place=values["place"], lat=values["geometry"][0], lon=values["geometry"][1], 
                                   dist=value["distance"], display_name = value["display_name"],
                                   duration = value["duration"], estimate = value["estimate"],
                                   high_estimate = value["high_estimate"], low_estimate = value["low_estimate"],
                                   autotime=values["autotime"], time=values["time"],
                                      day=values["day"], company="Uber"
                                  ))
    # commit() flushes whatever remaining changes remain to the database, and commits the transaction.
    # print("uber done")
    session1.commit()

    
    
    
       
    
for i in range(96):
    print(i)
    try:
        collect_lyft_data()
    except:
        print("Lyft needs authentication")
        
    try:
        collect_uber_data()
    except:
        print("Uber needs attention")
        
    if i != 95:
        time.sleep(240)