from flask import (
   Flask, 
   render_template, 
   request,  
   flash
)

from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup, SoupStrainer
import requests
import pandas as pd



# Create the Flask Instance
app = Flask(__name__)


@app.route("/", methods=("GET", "POST"), strict_slashes=False)
def index():
   # Parsing Code will go here
   if request.method == "POST":
      try:
         global url, specific_element

         url = "https://www.cbssports.com/nfl/injuries/daily"

         only_tr = SoupStrainer('tr')
         source = requests.get(url).text
         soup = BeautifulSoup(source, 'lxml', parse_only=only_tr)

         # Find the number of lines to add to the table
         specific_element = soup.find_all('tr', limit=16)[1:]
 

         return render_template("index.html",
                                results=specific_element
                                )

      except Exception as e:
         flash(e, 'danger')

   return render_template('index.html')


@app.route("/replays/")
def replays():
   return render_template('replays.html')

@app.route("/stats/")
def stats():
   return render_template('stats.html')

@app.route("/algorithm/")
def algorithm():
   return render_template('algorithm.html')

@app.route("/design/")
def design():
   return render_template('design.html')

@app.route("/delivery/")
def delivery():
   return render_template('delivery.html')

@app.route("/report/")
def report():
   return render_template('report.html')


if __name__ == "__main__":
   app.run(debug=True)
