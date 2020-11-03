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
from config.py import DATABASE_URL


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

engine = create_engine(DATABASE_URL)
connection = engine.connect()
cursor = connection.cursor()

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    message = "Welcome to my 'Home' page!"
    return render_template("index.html", message = message)


@app.route("/data")
def data():
    data = pd.read_sql("SELECT * FROM contributions_2018 WHERE state = Alabama and candidate = 'Write in';" con = connection)
    data_dict=data.to_dict(orient="records")
    return jsonify(data_dict)


    # cursor.execute("select * from table_name") 
    # data = cursor.fetchall() #data from database 
    # return render_template("example.html", value=data)
    # print("Server received request for 'Home' page...")
    # return "Welcome! This is the analysis of the Campaign Finance Contribution In United States Senate!"
# @app.route("/about")
# def about():
#     print("Server received request for 'About' page...")
#     message = "Welcome to my 'About' page!"
#     data = pd.read_sql(SELECT * FROM votersinfo
#      WHERE state = "Alabama" and candidate = "Write in"; conn = connection)

#     return render_template("index.html", message = message, data = data.to_html())


if __name__ == "__main__":
    app.run(debug=True)