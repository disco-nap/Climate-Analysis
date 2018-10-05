import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
from datetime import date

# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)



# Flask Routes

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    precip_year = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date.between('2016-01-01', '2017-01-01')).all()

    precip = dict(precip_year)

    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    #Return a JSON list of stations from the dataset.
    stations = session.query(func.distinct(Measurement.station)).all()

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    #Return a JSON list of Temperature Observations (tobs) for the previous year.
    temps = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date.between('2016-01-01' , '2017-01-01')).all()

    temp = dict(temps)

    return jsonify(temp)

@app.route("/api/v1.0/<start>")
def since():
    #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    #When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')

    last_date = dt.datetime.strptime('2017-08-23', '%Y-%m-%d')

    summary_since_start = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date.between(start_date, last_date)).all()

    return jsonify(summary_since_start)

@app.route("/api/v1.0/<start>/<end>")
def between():
    #When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')

    end_date = dt.datetime.strptime(end, '%Y-%m-%d')

    summary_start_end = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date.between (start_date, end_date)).all()

    return jsonify(summary_start_end)

if __name__ == '__main__':
    app.run(debug=True)