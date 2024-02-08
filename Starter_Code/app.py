# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

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
    """List all available api routes."""
    return f"Available Routes:<br/>" f"/api/v1.0/precipitation<br/>" f"/api/v1.0/stations<br/>" f"/api/v1.0/tobs<br/>" f"/api/v1.0/start<br/>" f"/api/v1.0/start/end<br/>"


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Calculate the date one year from the last date in data set.
    one_year = dt.date(2017,8,23)-dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=one_year).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Station.station).all()

    session.close()

    stations = list(np.ravel(results))

    return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    most_active_station_id = "USC00519281"
    
     # Query all passengers
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Query the temperature observations for the most active station within the last 12 months
    results = session.query(Measurement.tobs).filter(Measurement.station == most_active_station_id).filter(Measurement.date >= one_year_ago).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def Masha(start=None, end=None):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    sel=[func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    """Return a list of all passenger names"""
    # Query all passengers
    if not end: 
        start = dt.datetime.strptime(start, '%Y%m%d')
        results = session.query(*sel).filter(Measurement.date >= start).all()

        session.close()

        # Convert list of tuples into normal list
        all_names = list(np.ravel(results))
        return jsonify(all_names)
    
    start = dt.datetime.strptime(start, '%Y%m%d')
    end = dt.datetime.strptime(end, '%Y%m%d')
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))
    return jsonify(all_names)




if __name__ == "__main__":
    app.run(debug=True)


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file

# Declare a Base using `automap_base()`

# Use the Base class to reflect the database tables


# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`


# Create a session


#################################################
# Flask Setup
#################################################


#################################################
# Flask Routes
#################################################
