from flask import Flask, render_template, redirect
import pymongo
#from flask_pymongo import PyMongo
import scrape_mars
import sys

#setup Flask
app = Flask(__name__)

#the default port used by MongoDB is 27017
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

#Define the 'classDB' database in Mongo & collection
db = client.mars
collection = db.mars


@app.route("/")
def index():
    mars = db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = db.mars
    nasa_mars_data = scrape_mars.scrape_all()
    mars.update({}, nasa_mars_data, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)