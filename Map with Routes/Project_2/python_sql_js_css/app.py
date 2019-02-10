import json
import pandas as pd
import numpy as np
import os
import sqlalchemy

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import func
from sqlalchemy import distinct

from flask import Flask, render_template
from flask import Flask, jsonify

import threading
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///UberPrices.sqlite")
engine2 = create_engine("sqlite:///ClosebyPlaces.sqlite")
# reflect an existing database into a new model
Base = automap_base()
Base2 = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
Base2.prepare(engine2, reflect=True)
# Save reference to the table
UberPrices = Base.classes.uberPrices
ClosebyPlaces = Base2.classes.closebyPlaces
# Create our session (link) from Python to the DB
session = Session(engine)
session2 = Session(engine2)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#@app.route("/")
#def welcome():
 #   """List all available api routes."""
 #   return (
 #       f"Available Routes:<br/>"
 #       f"/api/v1.0/names<br/>"
 #       f"/api/v1.0/passengers"
 #   )

#@app.route("/api/v1.0/names")
#def names():
   # """Return a list of all passenger names"""
    # Query all passengers
    #results = session.query(UberPrices.place, UberPrices.lat, UberPrices.lon, UberPrices.dist, UberPrices.display_name, 
    #                        UberPrices.product_id, UberPrices.duration, UberPrices.estimate).all()

    # Convert list of tuples into normal list
    #all_names = list(np.ravel(results))

    #return jsonify(results)


#@app.route("/api/v1.0/passengers")
#def passengers():
    #"""Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    #results = session.query(Passenger).all()

    # Create a dictionary from the row data and append to a list of all_passengers
    #all_passengers = []
    #for passenger in results:
    #    passenger_dict = {}
    #    passenger_dict["name"] = passenger.name
     #   passenger_dict["age"] = passenger.age
    #    passenger_dict["sex"] = passenger.sex
    #    all_passengers.append(passenger_dict)

    #return jsonify(all_passengers)

results = session.query(UberPrices.place, UberPrices.lat, UberPrices.lon, UberPrices.dist, UberPrices.display_name, 
                           UberPrices.product_id, UberPrices.duration, UberPrices.estimate, UberPrices.time).all()
# count distinct "name" values
myplaces = session.query(distinct(UberPrices.place)).order_by(UberPrices.dist).all()
mytimes = session.query(distinct(UberPrices.time)).all()
mytypes = session.query(distinct(UberPrices.display_name)).all()

x = session.query(UberPrices.duration).all()
v = session.query(UberPrices.dist).all()

chartdata = session.query(UberPrices.place, UberPrices.duration, UberPrices.high_estimate, UberPrices.low_estimate, UberPrices.dist, UberPrices.time, UberPrices.display_name).all()
#chartdata2 = session.query(UberPrices.place, UberPrices.duration, UberPrices.high_estimate, UberPrices.low_estimate, UberPrices.dist, UberPrices.time, UberPrices.display_name).all()

nearbyplaces = session2.query(ClosebyPlaces.place, ClosebyPlaces.mlat, ClosebyPlaces.mlon, ClosebyPlaces.lat, ClosebyPlaces.lon, ClosebyPlaces.name, ClosebyPlaces.vicinity).all()
#below not working
#barchartdata = Session.query(UberPrices.place, UberPrices.duration, UberPrices.display_name, UberPrices.high_estimate, UberPrices.low_estimate, UberPrices.dist, #UberPrices.time).group_by(UberPrices.place).group_by(UberPrices.time).all()

#c.count = Session.query(func.count(Person.id)).scalar()
 
#c.avg = Session.query(func.avg(Person.id).label('average')).scalar()
       
#c.sum = Session.query(func.sum(Person.id).label('sum')).scalar()
        
#c.max = Session.query(func.max(Person.id).label('max')).scalar() 
        
#c.coutg = Session.query(func.count(Person.id).label('count'), Person.name ).group_by(Person.name).all()
@app.route("/placesinfo")
def placesinfo():
    #results = session.query(UberPrices.place, UberPrices.lat, UberPrices.lon, UberPrices.dist, UberPrices.display_name, 
    #                       UberPrices.product_id, UberPrices.duration, UberPrices.estimate).all()
    # data = db.session.query(uberPrices).all()
    return jsonify(nearbyplaces)

@app.route("/chartsinfo")
def chartsinfo():
    total_chart_info = [ myplaces, mytimes, mytypes, chartdata]
    
    return jsonify(total_chart_info)


@app.route("/data")
def data():
    #results = session.query(UberPrices.place, UberPrices.lat, UberPrices.lon, UberPrices.dist, UberPrices.display_name, 
    #                       UberPrices.product_id, UberPrices.duration, UberPrices.estimate).all()
    data = jsonify(results)
    
    # data = db.session.query(uberPrices).all()
    return jsonify(results)
    #return render_template("index.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/map")
def map():
    return render_template("map.html")

@app.route("/chart5")
def chart5():
    return render_template("chart5.html")

@app.route("/chart")
def chart():
    # Create a dictionary from the row data and append to a list of chartinfo
    chartinfo = []
    for data in chartdata:
        data_dict = {}
        data_dict["place"] = data.place
        data_dict["duration"] = data.duration
        data_dict["high_estimate"] = data.high_estimate
        data_dict["low_estimate"] = data.low_estimate
        data_dict["distance"] = data.dist
        data_dict["time"] = data.time
        chartinfo.append(data_dict)
    
    #return jsonify(all_passengers)
    return render_template("chart.html", chartdata = chartdata, chartinfo = chartinfo)

@app.route("/chart2")
def chart2():
    # Create a dictionary from the row data and append to a list of chartinfo
    chartinfo = []
    for data in chartdata:
        data_dict = {}
        data_dict["place"] = data.place
        data_dict["duration"] = data.duration
        data_dict["high_estimate"] = data.high_estimate
        data_dict["low_estimate"] = data.low_estimate
        data_dict["distance"] = data.dist
        data_dict["time"] = data.time
        chartinfo.append(data_dict)
    #rows = session.query(Person).count()
    times = []
    for time in mytimes:
        times.append(time[0])
    
    places = []
    for place in myplaces:
        places.append(place[0])
    
    types = []
    for type in mytypes:
        types.append(type[0])
        
        
    
    #return jsonify(all_passengers)
    return render_template("chart2.html", chartdata = chartdata, chartinfo = chartinfo, places = places, times = times, types = types)

@app.route("/chart3")
def chart3():
    # Create a dictionary from the row data and append to a list of chartinfo
    chartinfo = []
    for data in chartdata:
        data_dict = {}
        data_dict["place"] = data.place
        data_dict["duration"] = data.duration
        data_dict["high_estimate"] = data.high_estimate
        data_dict["low_estimate"] = data.low_estimate
        data_dict["distance"] = data.dist
        data_dict["time"] = data.time
        chartinfo.append(data_dict)
    #rows = session.query(Person).count()
    times = []
    for time in mytimes:
        times.append(time[0])
    
    places = []
    for place in myplaces:
        places.append(place[0])
    
    types = []
    for type in mytypes:
        types.append(type[0])
        
        
    
    #return jsonify(all_passengers)
    return render_template("chart3.html", chartdata = chartdata, chartinfo = chartinfo, places = places, times = times, types = types)


if __name__ == "__main__":
    app.run(debug=True)