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

   # # Establish the connection to the url
   # executable_path = {'executable_path': ChromeDriverManager().install()}
   # browser = Browser('chrome', **executable_path, headless=True)

   # Visit the webpage
   # url = "https://www.cbssports.com/nfl/injuries/daily"
   # browser.visit(url)

   # Convert the browser html to a soup object
   # html = browser.html
   # parsed_html = BeautifulSoup(html, 'lxml')

   url = "https://www.cbssports.com/nfl/injuries/daily"
   source = requests.get(url)
   soup = BeautifulSoup(source.text, 'html.parser')

   data = soup.find('tr')
   table_data = []
   trs = soup.select('tr.TableBase-bodyTr')
   
   for tr in trs[1:16]:
      row = []
      for t in tr.select('td')[0:4]:
         row.extend([t.text])
      table_data.append(row)

   data = table_data


   
   return render_template('index.html', data=data)




   # # Create empty lists
   # player = []
   # position = []
   # injury = []
   # team = []
   # logo = []

   # # # Add try/except for error handling
   # # try:
   # #    slide_elem = parsed_html.select('tr.TableBase-bodyTr')
   # #    # Find all of the Tr rows
   # #    rows = parsed_html.findAll('tr', limit=16)[1:]  # the 0th tr is headers
   # # except AttributeError:
   # #    return None, None


   # # Get info from each row
   # for i in range(len(rows)):
   #    player.append(slide_elem[i].find(
   #       'span', class_='CellPlayerName--long').get_text())
   #    position.append(slide_elem[i].find(
   #       'td', class_='TableBase-bodyTd').next_sibling.next_sibling.get_text().strip())
   #    injury.append(slide_elem[i].find(
   #       'td', class_='TableBase-bodyTd').next_sibling.next_sibling.next_sibling.get_text().strip())
   #    team.append(slide_elem[i].find('span', class_='TeamName').get_text())
   #    logo.append(slide_elem[i].find(
   #       'img', class_='TeamLogo-image').get('src'))

   # data = pd.DataFrame({
   #    'Logo': logo,
   #    'Team': team,
   #    'Player': player,
   #    'Position': position,
   #    'Injury': injury
   # })

   # browser.quit()
   # return render_template('index.html', data=data)


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
