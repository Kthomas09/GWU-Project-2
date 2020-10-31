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

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/cars_api"
db = SQLAlchemy(app)
GWU = create_classes(db)



# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    # print("Server received request for 'Home' page...")
    # return "Welcome! This is the analysis of the Campaign Finance Contribution In United States Senate!"
    return render_template("index.html")


@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        # name = request.form["petName"]
        # lat = request.form["petLat"]
        # lon = request.form["petLon"]

        year =request.form["year"]
        state= request.form["state"]
        state_po= request.form["state_po"]
        candidate= request.form["candidate"]
        party = request.form["party"]
        candidatevotes = request.form["candidatevotes"]
        writein =request.form["writein"]
        totalvotes =request.form["totalvotes"]

	# Committee 
  	# SubComittee 
   	# Chair_Names 
   	# Party 
  	# State 
   	# Ranking_Members 

	# First_Name 
	# Last_Name	
 	# State	
 	# Party_Name	
 	# Total_Raised 
 	# Full_Name 
 	# State_Abbrv	
 	# Party 

    # First_Name 
	# Last_Name	
 	# State	
 	# Party_Name	
 	# Total_Raised 
 	# Full_Name 
 	# State_Abbrv	
 	# Party 

    #         First_Name 
	# Last_Name	
 	# State	
 	# Party_Name	
 	# Total_Raised 
 	# Full_Name 
 	# State_Abbrv	
 	# Party 


        gwu = GWU(year=year, state=state, state_po=state_po,candidate=candidate,party=party,
        candidatevotes=candidatevotes,writein=writein,totalvotes=totalvotes)
        db.session.add(GWU)
        db.session.commit()
        return redirect("/", code=302)

    return render_template("form.html")
# 4. Define what to do when a user hits the /about route
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"


if __name__ == "__main__":
    app.run(debug=True)