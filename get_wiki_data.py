import requests
from bs4 import BeautifulSoup
import sqlite3

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/Formula_One"

# Connect to the SQLite database
conn = sqlite3.connect("data.db")
cursor = conn.cursor()


# Fetch the Wikipedia page
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Scrape qualifying results table
qualifying_table = soup.find("table", class_="wikitable")
qualifying_rows = qualifying_table.find_all("tr")[1:]  # Skip header row

for row in qualifying_rows:
    columns = row.find_all("td")
    driver = columns[1].text.strip()
    team = columns[2].text.strip()
    position = int(columns[0].text.strip())
    time = columns[3].text.strip()

    # Insert qualifying result into the database
    cursor.execute("""
        INSERT INTO qualifying_results (driver, team, position, time)
        VALUES (?, ?, ?, ?)
    """, (driver, team, position, time))

# Scrape race results table
race_table = soup.find_all("table", class_="wikitable")[1]
race_rows = race_table.find_all("tr")[1:]  # Skip header row

for row in race_rows:
    columns = row.find_all("td")
    driver = columns[1].text.strip()
    team = columns[2].text.strip()
    position = int(columns[0].text.strip())
    time = columns[3].text.strip()

    # Insert race result into the database
    cursor.execute("""
        INSERT INTO race_results (driver, team, position, time)
        VALUES (?, ?, ?, ?)
    """, (driver, team, position, time))

# Commit the changes and close the connection
conn.commit()
conn.close()
