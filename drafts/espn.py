import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Setting up headless Chrome options
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

# Initializing the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Navigating to the initial URL
driver.get("https://www.espn.com/nba/teams")

# Find all elements with the text 'Statistics'
statistics_links = driver.find_elements(By.LINK_TEXT, "Statistics")

# Extract the URLs
statistics_urls = [link.get_attribute('href') for link in statistics_links]

# Initialize a set to store unique player URLs
unique_player_urls = set()

# Navigate to each URL in the 'statistics_urls' list and scrape player links
for url in statistics_urls:
    driver.get(url)
    player_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/nba/player/_/id/')]")
    for player_link in player_links:
        unique_player_urls.add(player_link.get_attribute('href'))

# Initialize a list to store the scraped URLs
scraped_urls = []

# Navigate to each player URL and scrape specific URLs
for player_url in unique_player_urls:
    driver.get(player_url)
    div_elements = driver.find_elements(By.CSS_SELECTOR, "div.Card__Header__SubLink__Text a")
    for element in div_elements:
        url = element.get_attribute('href')
        scraped_urls.append(url)
        print(url)

# Close the driver
driver.quit()

# Write the scraped URLs to a CSV file
csv_file = 'extracted_urls.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for url in scraped_urls:
        writer.writerow([url])

print(f"Scraped URLs have been saved to {csv_file}.")
