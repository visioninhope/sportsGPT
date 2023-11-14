from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
from psycopg2 import sql

chrome_options = Options()
chrome_options.add_argument('--headless')

def scrape_players_data(url):
    # Setup Selenium ChromeDriver
    service = Service(ChromeDriverManager().install())
    # driver = webdriver.Chrome(service=service)
    driver = webdriver.Chrome(options=chrome_options)
    # Fetch the content from the URL
    driver.get(url)

    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the table rows with the class 'full_table' which contains the players data
    player_rows = soup.find_all('tr', class_='full_table')

    # Define the headers
    headers = [
        "Player", "Position", "Age", "Team", "Games", "GamesStarted",
        "MinutesPlayed", "FieldGoals", "FieldGoalsAttempted", "FieldGoalPercentage",
        "ThreePointers", "ThreePointersAttempted", "ThreePointPercentage", 
        "TwoPointers", "TwoPointersAttempted", "TwoPointersPercentage",
        "EffectiveFieldGoalPercentage", "FreeThrows", "FreeThrowsAttempted", 
        "FreeThrowsPercentage", "OffensiveRebounds", "DefensiveRebounds", 
        "TotalRebounds", "Assists", "Steals", "Blocks", "Turnovers", 
        "PersonalFouls", "Points", "Salary", "Season", "SeasonEnd"
    ]

    # Extract players data
    players_data = []
    for row in player_rows:
        # Extract each cell from the row
        cells = row.find_all('td')
        player_info = [cell.get_text(strip=True) for cell in cells]
        if player_info:
            players_data.append(player_info)

    # Convert the data to a DataFrame
    df_players = pd.DataFrame(players_data, columns=headers)

    # Close the driver
    driver.quit()

    return df_players

def insert_into_database(df, hostname, username, password, database):
    # Connect to the database
    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
    cursor = conn.cursor()

    # Insert data into the database
    for index, row in df.iterrows():
        cursor.execute(
            sql.SQL("INSERT INTO players (" + ", ".join(df.columns) + ") VALUES (%s)" + ", %s" * (len(df.columns) - 1)),
            tuple(row)
        )

    # Commit changes and close connection
    conn.commit()
    cursor.close()
    conn.close()

# URL to scrape
url = 'https://www.basketball-reference.com/leagues/NBA_2024_per_game.html'

# Scrape the data
df_players = scrape_players_data(url)

# Database credentials (replace with your actual credentials)
hostname = 'localhost'
username = 'sportsgpt'
password = 'sportsgpt'
database = 'sportsgptdb'

# Insert data into PostgreSQL database
insert_into_database(df_players, hostname, username, password, database)
