import os
import pandas as pd
from dotenv import load_dotenv
from scraper.scraper import scrape, signin

# Load environment variables
load_dotenv()

# Load the ID and usernames mapping
df = pd.read_csv('data/congress_id_names.csv')
usernames = df['Username'].tolist()

# Authenticate the scraper session
username = os.environ.get("TWITTER_USERNAME")
password = os.environ.get("TWITTER_PASSWORD")
scraper = signin(username=username, password=password)

# Get a list of already scraped user IDs
output_folder = "data/congress_tweets"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
already_scraped_ids = [filename.split('_')[0] for filename in os.listdir(output_folder)]

try:
    for username in usernames:
        # Get the user ID from the username
        user_id = df.loc[df['Username'] == username, 'Id'].values[0]

        # Check if this user's tweets have already been scraped
        if str(user_id) in already_scraped_ids:
            continue  # Skip scraping for this user

        # Perform the scraping
        scrape(
            scraper=scraper,
            query=f'(from:@{username}) until:2022-06-09 since:2022-03-01',
            tweets=999
        )
except Exception as e:
    print(e)
finally:
    scraper.driver.close()
