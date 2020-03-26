# 1. import Flask
from flask import Flask, jsonify

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# Import Dependencies
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import and_
import sqlalchemy.pool as pool
import datetime as dt

# Database

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Define what to do when a user hits home page
@app.route("/")
def home():
    return"""<html>
    <h1>List of all available routes:</h1>
    <ul>
    <br>
    <li>
    Return daily precipitation levels from last year:
    <br>
    <a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a>
    </li>
    <br>
    <li>
    Return a JSON list of stations from the dataset: 
    <br>
   <a href="/api/v1.0/stations">/api/v1.0/stations</a>
   </li>
    <br>
    <li>
    Return a JSON list of Temperature Observations (tobs) for one year from latest point in dataset:
    <br>
    <a href="/api/v1.0/tobs">/api/v1.0/tobs</a>
    </li>
    <br>
    <li>
    Return a JSON list of tmin, tmax, tavg for the dates in range greater than or equal to start date:
    <br>
    Replace &ltstart&gt and &ltend&gt with a date in Year-Month-Day format. 
    <br>
    <a href="/api/v1.0/2012-02-28">/api/v1.0/2012-02-28</a>
    </li>
    <br>
    <li>
    Return a JSON list of tmin, tmax, tavg for the dates in range of start date and end date inclusive:
    <br>
    Replace &ltstart&gt and &ltend&gt with a date in Year-Month-Day format. 
    <br>
    <a href="/api/v1.0/2016-04-23/2016-04-30">/api/v1.0/2016-04-23/2016-04-30</a>
    </li>
    <br>
    </ul>
    </html>
    """

# Define what to do when a user hits precipitation route

@app.route("/api/v1.0/precipitation")

def precipitation():
    """Query for the dates and temperature observations from the last year.
    Convert the query results to a Dictionary using date as the 'key 'and 'tobs' as the value."""
    
    # Calculate & define dates

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = last_date[0]

    query_date = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days = 365)
    query_date.strftime("%Y-%m-%d")

    # Perform a query to retrieve the data and avg precipitation scores
    sel = [Measurement.date, func.avg(Measurement.prcp)]

    prcp_data = session.query(*sel).\
        filter(Measurement.date >= query_date).\
        filter(Measurement.date <= last_date).\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()

    # Create a dictionary from the row data and append to a list of for the precipitation data
    precipitation_data = []
    for date, prcp in prcp_data:
        prcp_data_dict = {}
        prcp_data_dict["Date"] = date
        prcp_data_dict["Precipitation"] = prcp
        precipitation_data.append(prcp_data_dict)
        
    return jsonify(precipitation_data)

# Define what to do when a user hits stations route
@app.route("/api/v1.0/stations")
def stations():
    """Return a json list of stations from the dataset."""
    # Query all the stations
    total_stations = session.query(Station.station, Station.name).all()

    # Create a dictionary from the row data and append to a list of all_stations.
    total_stations_dict = []
    for station, name in total_stations:
        stations_dict = {}
        stations_dict["Station"] = station
        stations_dict["Station Name"] = name
        total_stations_dict.append(stations_dict)

    return jsonify(total_stations_dict)

# Define what to do when a user hits tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    """query for the dates and temperature observations from a year from the last data point."""
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""

    # Calculate & define dates

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = last_date[0]

    query_date = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days = 365)
    query_date.strftime("%Y-%m-%d")
    
    # Perform a query to retrieve the data and avg tobs levels
    sel = [Measurement.date, func.avg(Measurement.tobs)]

    tobs_data = session.query(*sel).\
        filter(Measurement.date >= query_date).\
        filter(Measurement.date <= last_date).\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()

    # Create a dictionary from the row data and append to a list of for the precipitation data
    temp_data = []
    for date, tobs in tobs_data:
        tobs_data_dict = {}
        tobs_data_dict["Date"] = date
        tobs_data_dict["Tobs"] = tobs
        temp_data.append(tobs_data_dict)
        
    return jsonify(temp_data)

# # Define what to do when a user hits trip route
@app.route("/api/v1.0/2012/02/28")
def tripstart():  
    trip_start_date = 2/28/2012

    # Perform a query to retrieve the data and tmin, tmax, tavg levels for dates great than or equal to start date
    sel = [Measurement.date, func.avg(Measurement.tobs)]

    start_date_data = session.query(*sel).\
        filter(Measurement.date >= trip_start_date).\
        group_by(Measurement.date).\
        order_by(desc(func.avg(Measurement.tobs))).all()

    start_date_info = []
    for tmin, tmax, tavg in start_date_data:
        start_date_dict = {}
        start_date_dict["tmin"] = tobs.min()
        start_date_info.append(start_date_dict)
    return jsonify(start_date_info)

# # Define what to do when a user hits trip route
@app.route("/api/v1.0/<trip_start_date>&<trip_end_date>")
def trip(trip_start_date, trip_end_date):  

    # Calculate & define dates


if __name__ == "__main__":
    app.run(debug=True)
