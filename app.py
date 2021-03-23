import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
        return """<html>
<h1>Hawaii Climate App</h1>
<p>Precipitation:</p>
<ul>
  <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
</ul>
<p>Stations</p>
<ul>
  <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
</ul>
<p>Temperatures:</p>
<ul>
  <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
</ul>
<p>Start Day:</p>
<ul>
  <li><a href="/api/v1.0/2017-03-14">/api/v1.0/2017-03-14</a></li>
</ul>
<p>Start & End Day:</p>
<ul>
  <li><a href="/api/v1.0/2017-03-14/2017-03-28">/api/v1.0/2017-03-14/2017-03-28</a></li>
</ul>
</html>
"""

# Precipitation Route
@app.route("/api/v1.0/precipitation")
def precipitation():
      session = Session(engine)
        # Convert the query results to a dictionary using `date` as the key and `prcp` as the value
      prcp = session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()
      session.close()
        # Convert into a dictionary
      prcp_list = dict(prcp)
        # Return JSON representation of dictionary
      return jsonify(prcp_list)

# Stations Route
@app.route("/api/v1.0/stations")
def stations():
      session = Session(engine)
        # Return a JSON List of Stations From the Dataset
      stations_all = session.query(Station.station, Station.name).all()
      session.close()
        # Convert into list
      station_list = list(stations_all)
        # Return JSON List of Stations from the Dataset
      return jsonify(station_list)

# TOBs Route
@app.route("/api/v1.0/tobs")
def tobs():
      session = Session(engine)
        # Query the dates and temperature observations of the most active station for the last year of data
      one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
      tobs_data = session.query(Measurement.date, Measurement.tobs).\
              filter(Measurement.date >= one_year_ago).\
              order_by(Measurement.date).all()
      session.close()
        # Convert into list
      tobs_data_list = list(tobs_data)
        # Return a JSON list of temperature observations (TOBS) for the previous year
      return jsonify(tobs_data_list)

# Start Day Route
@app.route("/api/v1.0/<start>")
def start_day(start):
      session = Session(engine)
      # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
      start_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), 
      func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).\
              group_by(Measurement.date).all()
      session.close()
        # Convert list
      start_day_list = list(start_day)
        # Return a JSON list of the minimum temperature, the average temperature, and the max temperature 
        # for a given start or start-end range
      return jsonify(start_day_list)

# Start-End Day Route
@app.route("/api/v1.0/<start>/<end>")
def start_end_day(start, end):
      session = Session(engine)
      # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive
      start_end_day = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), 
      func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).\
              filter(Measurement.date <= end).\
              group_by(Measurement.date).all()
      session.close()
        # Convert list
      start_end_day_list = list(start_end_day)
        # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range
      return jsonify(start_end_day_list)

if __name__ == '__main__':
    app.run(debug=True)