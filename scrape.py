# Import the necessary libraries
import requests
from bs4 import BeautifulSoup


# web scraping function to get song names fr
def scrape_website(url):
    # Make a GET request to the specified URL
    response = requests.get(url)

    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the song names from the page
    song_names = []
    rows = soup.find_all('div', class_='o-chart-results-list-row-container')
    for row in rows:
        song = row.find('h3', class_='c-title').text
        song_names.append(song.strip())

    return song_names
