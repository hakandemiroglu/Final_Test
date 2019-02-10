import json
import pandas as pd
import numpy as np
import os
import gmaps

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, render_template
from flask import Flask, jsonify

from uber_rides.session import Session
session_uber = Session(server_token="TZ9aAN7GMzp49djfXoMil2HJ7XxCs0Zwo8EWXd88")
from uber_rides.client import UberRidesClient
client = UberRidesClient(session_uber)

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
total_estimates = []
estimates = {}

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
    estimates["value"] = estimate
    total_estimates.append(estimates)
#total_estimates

import json
with open('outfile.json', 'w') as outfile:
    json.dump(total_estimates, outfile)

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Define our pet table
class UberPrices(Base):
    __tablename__ = 'uberPrices'
    id = Column(Integer, primary_key=True)
    place = Column(String)
    lat = Column(Integer)
    lon = Column(Integer)
    dist = Column(Integer)
    display_name = Column(String)
    product_id = Column(String)
    duration = Column(Integer)
    estimate = Column(String)

# Right now, this table only exists in python and not in the actual database
# Base.metadata.tables

# Create our database engine
engine = create_engine('sqlite:///UberPrices.sqlite')

# This is where we create our tables in the database
Base.metadata.create_all(engine)

# The ORM’s “handle” to the database is the Session.
from sqlalchemy.orm import Session
session = Session(engine)

# Note that adding to the session does not update the table. It queues up those queries.
for values in total_estimates:
    for value in values["value"]:
        session.add(UberPrices(place=values["place"], lat=values["geometry"][0], lon=values["geometry"][1], dist=value["distance"],
                               display_name = value["display_name"], product_id = value["product_id"], duration = value["duration"],
                              estimate = value["estimate"]))
# commit() flushes whatever remaining changes remain to the database, and commits the transaction.
session.commit()

#################################################
# Database Setup
#################################################
#engine = create_engine("sqlite:///UberPrices.sqlite")

# reflect an existing database into a new model
#Base = automap_base()
# reflect the tables
#Base.prepare(engine, reflect=True)

# Save reference to the table
#UberPrices = Base.classes.uberPrices

# Create our session (link) from Python to the DB
#session = Session(engine)

#################################################
