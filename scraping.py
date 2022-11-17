# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_injuries():
    # Scrape CBS NFL Daily Injuries
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Visit the webpage
    url = "https://www.cbssports.com/nfl/injuries/daily"
    browser.visit(url)

    # Convert the browser html to a soup object
    html = browser.html
    parsed_html = soup(html, 'lxml')

    # Create empty lists
    player = []
    position = []
    injury = []
    team = []
    logo = []

    # Add try/except for error handling
    try:
        slide_elem = parsed_html.select('tr.TableBase-bodyTr')
        # Find all of the Tr rows
        rows = parsed_html.findAll('tr', limit=21)[1:]  # the 0th tr is headers

    except AttributeError:
        return None, None


    # Get info from each row
    for i in range(len(rows)):
        player.append(slide_elem[i].find(
            'span', class_='CellPlayerName--long').get_text())
        position.append(slide_elem[i].find(
            'td', class_='TableBase-bodyTd').next_sibling.next_sibling.get_text().strip())
        injury.append(slide_elem[i].find(
            'td', class_='TableBase-bodyTd').next_sibling.next_sibling.next_sibling.get_text().strip())
        team.append(slide_elem[i].find('span', class_='TeamName').get_text())
        logo.append(slide_elem[i].find('img', class_='TeamLogo-image').get('src'))

    recent_injuries = pd.DataFrame({
        'Logo': logo,
        'Team': team,
        'Player': player,
        'Position': position,
        'Injury': injury
    })

    return recent_injuries.to_html(classes="table table-hover")



if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_injuries())

