import os

import pandas as pd
from dotenv import load_dotenv
from datetime import timedelta

from scraper.scraper import signin, scrape
from utils.post_scraping import post_scraping


def should_skip_file(df, skip_date="2022-03-01"):
    if not df.empty:
        last_timestamp_date = pd.to_datetime(df['Timestamp'].iloc[-1]).date()
        if last_timestamp_date == pd.to_datetime(skip_date).date():
            return True
    return False


def process_file(file_path, current_index, total_files, scraper):
    df = pd.read_csv(file_path)

    if should_skip_file(df):
        print(f"[{current_index}/{total_files}] Skipped {file_path} based on skip conditions.")
        return False

    # Get the last timestamp from the file
    last_timestamp = df['Timestamp'].iloc[-1]

    # Get the user ID and username from the file name
    user_id = os.path.basename(file_path).split('_')[0]
    id_names = pd.read_csv('data/congress_id_names.csv')
    username = id_names.loc[id_names['Id'] == int(user_id), 'Username'].values[0]

    # Stage 1: Scrape 10 tweets from the last timestamp to 2022-03-01
    num_tweets = scrape(
        scraper=scraper,
        query=f'(from:@{username}) until:{last_timestamp} since:2022-03-01',
        tweets=10,
        to_csv=False
    )

    # If the scraper returns tweets, proceed to stage 2
    if num_tweets > 0:
        # Subtract one day from the last timestamp
        previous_day = pd.to_datetime(last_timestamp) + timedelta(days=1)
        previous_day_str = previous_day.strftime('%Y-%m-%d')

        # Stage 2: Scrape all tweets from the day after the last timestamp to 2022-03-01
        scrape(
            scraper=scraper,
            query=f'(from:@{username}) until:{previous_day_str} since:2022-03-01',
            tweets=9999,
        )

        print(
            f"[{current_index}/{total_files}] Kept {file_path} and appended new tweets found after the last timestamp.")
        return True

    # If the scraper returns no tweets, keep the file
    print(f"[{current_index}/{total_files}] Kept {file_path} as no new tweets were found.")
    return True


def main():
    # Authenticate the scraper session
    username = os.environ.get("TWITTER_USERNAME")
    password = os.environ.get("TWITTER_PASSWORD")
    scraper = signin(username=username, password=password)

    if not scraper:
        return

    directory = "../data/congress_tweets/"
    files = os.listdir(directory)
    total_files = len(files)

    try:
        for index, filename in enumerate(files[::-1], start=1):
            file_path = os.path.join(directory, filename)
            process_file(file_path, index, total_files, scraper)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        post_scraping()


load_dotenv()
main()
