from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/injuries_app"
mongo = PyMongo(app)


@app.route("/")
def index():
   mars = mongo.db.injuries.find_one()
   return render_template("index.html", injuries=injuries)


@app.route("/scrape")
def scrape():
   injuries = mongo.db.injuries
   injury_data = scraping.scrape_all()
   injuries.update_one({}, {"$set": injury_data}, upsert=True)
   return redirect('/', code=302)


if __name__ == "__main__":
   app.run()
