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

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Define our uberPrices table
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
    
engine = create_engine('sqlite:///LyftPricesNew.sqlite')
Base.metadata.create_all(engine)

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
   "location":[33.7850856,-84.373803]}]

for i in range(2):

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
        estimates["value"] = estimate
        # last_hour_date_time = datetime.now() - timedelta(hours = 1)
        # list_datetime_capture.append(last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S'))
        lyft_total_estimates.append(estimates)
    # lyft_total_estimates
    print(len(lyft_total_estimates))



    # Create our database engine
    engine = create_engine('sqlite:///LyftPricesNew.sqlite')

    # Base.metadata.create_all(engine)
    # The ORM’s “handle” to the database is the Session.
    from sqlalchemy.orm import Session
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
                                   autotime=values["autotime"], time=values["time"]
                                  ))

    # commit() flushes whatever remaining changes remain to the database, and commits the transaction.
    session.commit()
    time.sleep(60)