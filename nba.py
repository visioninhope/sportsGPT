from selenium import webdriver  # This line imports the webdriver module from selenium
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

def scrape_players_data(url, csv_file_path):
    # Setup Selenium ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Fetch the content from the URL
    driver.get(url)

    # Get the page source and parse it with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Find the table rows with the class 'full_table' which contains the players data
    player_rows = soup.find_all('tr', class_='full_table')

    # Extract players data
    players_data = []
    for row in player_rows:
        # Extract each cell from the row
        cells = row.find_all('td')
        player_info = [cell.get_text(strip=True) for cell in cells]
        if player_info:
            players_data.append(player_info)

    # Convert the data to a DataFrame
    df_players = pd.DataFrame(players_data)

    # Print the data to the terminal
    print(df_players)

    # Save the data to a CSV file
    df_players.to_csv(csv_file_path, index=False)

    # Close the driver
    driver.quit()

# URL and CSV file path
url = 'https://www.basketball-reference.com/leagues/NBA_2024_per_game.html'
csv_file_path = '/Users/bryan.wills/players.csv'

# Call the function to scrape and save data
scrape_players_data(url, csv_file_path)
