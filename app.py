from flask import Flask, render_template, request, flash
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup, SoupStrainer
import requests
import pandas as pd
import datetime as dt
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager



# Create the Flask Instance
app = Flask(__name__)


@app.route("/",  methods=("GET", "POST"), strict_slashes=False)
def index():

   url = "https://www.cbssports.com/nfl/injuries/daily"
   source = requests.get(url)
   soup = BeautifulSoup(source.text, 'html.parser')

   data = soup.find('tr')
   table_data = []
   trs = soup.select('tr.TableBase-bodyTr')
   

   for tr in trs[1:16]:
      row = []
      # row.extend([tr.find('img', class_='TeamLogo-image').get('src')])
      row.extend([tr.select('td')[0].text])
      row.extend([tr.find('span', class_='CellPlayerName--long').text])
      row.extend([tr.select('td')[2].text])
      row.extend([tr.select('td')[3].text])

      table_data.append(row)

   data = table_data


   return render_template('index.html', data=data)


@app.route("/replays/", methods=("GET", "POST"), strict_slashes=False)
def replays():
   return render_template('replays.html')


@app.route("/stats/", methods=("GET", "POST"), strict_slashes=False)
def stats():
   return render_template('stats.html')


@app.route("/algorithm/", methods=("GET", "POST"), strict_slashes=False)
def algorithm():
   return render_template('algorithm.html')


@app.route("/design/", methods=("GET", "POST"), strict_slashes=False)
def design():
   return render_template('design.html')


@app.route("/delivery/", methods=("GET", "POST"), strict_slashes=False)
def delivery():
   return render_template('delivery.html')


@app.route("/report/", methods=("GET", "POST"), strict_slashes=False)
def report():
   return render_template('report.html')


if __name__ == "__main__":
   app.run(debug=True)
