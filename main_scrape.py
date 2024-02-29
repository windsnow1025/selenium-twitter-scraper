import os
import random
import pandas as pd
from dotenv import load_dotenv
from scraper.scraper import scrape, signin
from utils.post_scraping import post_scraping


def get_users_to_scrape(usernames, id_names):
    # Get a list of already scraped user IDs
    output_folder = "data/congress_tweets"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    already_scraped_ids = [filename.split('_')[0] for filename in os.listdir(output_folder)]

    users_to_scrape = [username for username in usernames if str(id_names.loc[id_names['Username'] == username, 'Id'].values[0]) not in already_scraped_ids]
    return users_to_scrape


def main(scrape_new=True):
    # Load the ID and usernames mapping
    id_names = pd.read_csv('data/congress_id_names.csv')
    usernames = id_names['Username'].tolist()

    # Authenticate the scraper session
    username = os.environ.get("TWITTER_USERNAME")
    password = os.environ.get("TWITTER_PASSWORD")
    scraper = signin(username=username, password=password)

    if not scraper:
        return

    if scrape_new:
        usernames = get_users_to_scrape(usernames, id_names)

    try:
        random.shuffle(usernames)
        for index, username in enumerate(usernames, start=1):
            print(f"[{index}/{len(usernames)}] {username}")

            # Perform the scraping
            scrape(
                scraper=scraper,
                query=f'(from:@{username}) until:2022-06-09 since:2022-03-01',
                tweets=9999
            )
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        post_scraping()


load_dotenv()

while True:
    main(scrape_new=False)
