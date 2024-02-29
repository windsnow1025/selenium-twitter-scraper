import os
import pandas as pd
from dotenv import load_dotenv
from datetime import timedelta

from scraper.scraper import signin, scrape
from utils.post_scraping import post_scraping


def is_last_timestamp_at_start(df):
    if not df.empty:
        last_timestamp_date = pd.to_datetime(df['Timestamp'].iloc[-1]).date()
        if last_timestamp_date == pd.to_datetime("2022-03-01").date():
            return True
    return False


def no_tweets_since_last_timestamp(scraper, username, last_timestamp):
    num_tweets = scrape(
        scraper=scraper,
        query=f'(from:@{username}) until:{last_timestamp} since:2022-03-01',
        tweets=10,
        to_csv=False
    )

    if num_tweets > 0:
        return False

    return True


def process_file(file_path, current_index, total_files, scraper):
    df = pd.read_csv(file_path)

    if is_last_timestamp_at_start(df):
        print(f"[{current_index}/{total_files}] Skipped {file_path} as the last timestamp is 2022-03-01.")
        return False

    last_timestamp = df['Timestamp'].iloc[-1]

    user_id = os.path.basename(file_path).split('_')[0]
    id_names = pd.read_csv('data/congress_id_names.csv')
    username = id_names.loc[id_names['Id'] == int(user_id), 'Username'].values[0]

    if no_tweets_since_last_timestamp(scraper, username, last_timestamp):
        print(f"[{current_index}/{total_files}] Skipped {file_path} as no new tweets were found.")
        return False

    previous_day = pd.to_datetime(last_timestamp) + timedelta(days=1)
    previous_day_str = previous_day.strftime('%Y-%m-%d')

    scrape(
        scraper=scraper,
        query=f'(from:@{username}) until:{previous_day_str} since:2022-03-01',
        tweets=9999,
    )

    print(f"[{current_index}/{total_files}] Kept {file_path} and appended new tweets found after the last timestamp.")
    return True


def main():
    username = os.environ.get("TWITTER_USERNAME")
    password = os.environ.get("TWITTER_PASSWORD")
    scraper = signin(username=username, password=password)

    if not scraper:
        return

    directory = "data/congress_tweets/"
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

while True:
    main()