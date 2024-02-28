import os
import random
import pandas as pd
from dotenv import load_dotenv
from scraper.scraper import scrape, signin
from utils.process_id import process_id
from utils.remove_identical import remove_identical


def main():
    # Load the ID and usernames mapping
    df = pd.read_csv('data/congress_id_names.csv')
    usernames = df['Username'].tolist()

    # Authenticate the scraper session
    username = os.environ.get("TWITTER_USERNAME")
    password = os.environ.get("TWITTER_PASSWORD")
    scraper = signin(username=username, password=password)

    if not scraper:
        return

    # Get a list of already scraped user IDs
    output_folder = "data/congress_tweets"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    already_scraped_ids = [filename.split('_')[0] for filename in os.listdir(output_folder)]

    try:
        random.shuffle(usernames)
        for index, username in enumerate(usernames, start=1):
            print(f"[{index}/{len(usernames)}] {username}")

            # Get the user ID from the username
            user_id = df.loc[df['Username'] == username, 'Id'].values[0]

            # Check if this user's tweets have already been scraped
            if str(user_id) in already_scraped_ids:
                continue  # Skip scraping for this user

            # Perform the scraping
            scrape(
                scraper=scraper,
                query=f'(from:@{username}) until:2022-06-09 since:2022-03-01',
                tweets=9999
            )
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            # Process the scraped tweets
            process_id()
            # Remove identical timestamps
            remove_identical()
            # Remove the scraped tweets
            for filename in os.listdir('tweets'):
                os.remove(os.path.join('tweets', filename))
        except Exception as e:
            print(f"Error during processing: {e}")


# Load environment variables
load_dotenv()

while True:
    main()
