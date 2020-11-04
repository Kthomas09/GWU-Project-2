# 1. import Flask
from models import create_classes
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
from config import DATABASE_URL


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

engine = create_engine(DATABASE_URL)
connection = engine.connect()

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    message = "Welcome to my 'Home' page!"
    data_json= data().json
    return render_template("index.html", message = message, data= data_json)


@app.route("/data")
def data():
    data = pd.read_sql("SELECT * FROM votersinfo WHERE state = 'Alabama' and candidate = 'Write in';", con = connection)
    data_dict=data.to_dict(orient="records")
    return jsonify(data_dict)
   

# @app.route("/about")
# def about():
#     print("Server received request for 'About' page...")
#     message = "Welcome to my 'About' page!"
#     data = pd.read_sql("SELECT * FROM votersinfo WHERE state = Alabama and candidate = 'Write in';" con = connection)

#     return render_template("index.html", message = message, data = data.to_html())


if __name__ == "__main__":
    app.run(debug=True)