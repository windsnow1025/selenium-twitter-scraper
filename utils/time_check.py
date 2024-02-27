import os
import pandas as pd
from dotenv import load_dotenv

from scraper.scraper import signin, scrape


def should_skip_file(df, skip_date_1="2022-03-01", skip_date_2="2022-03-02", max_tweets_skip_date_2=100):
    if not df.empty:
        last_timestamp_date = pd.to_datetime(df['Timestamp'].iloc[-1]).date()
        total_tweets = df.shape[0]
        if last_timestamp_date == pd.to_datetime(skip_date_1).date():
            return True
        if last_timestamp_date == pd.to_datetime(skip_date_2).date() and total_tweets <= max_tweets_skip_date_2:
            return True
    return False


def should_delete_file(df, delete_after_date="2022-03-10", min_tweets=100, additional_delete_date="2022-03-20",
                       min_tweets_additional=50):
    if not df.empty:
        last_timestamp_date = pd.to_datetime(df['Timestamp'].iloc[-1]).date()
        total_tweets = df.shape[0]
        if last_timestamp_date > pd.to_datetime(delete_after_date).date() and total_tweets >= min_tweets:
            return True
        if last_timestamp_date > pd.to_datetime(
                additional_delete_date).date() and total_tweets >= min_tweets_additional:
            return True
    return False


def process_file(file_path, current_index, total_files, scraper):
    df = pd.read_csv(file_path)

    if should_delete_file(df):
        os.remove(file_path)
        print(
            f"[{current_index}/{total_files}] Deleted {file_path} due to it having a last timestamp after 2022-03-10 and at least 100 tweets.")
        return False

    if should_skip_file(df):
        print(f"[{current_index}/{total_files}] Skipped {file_path} based on skip conditions.")
        return False

    # Get the last timestamp from the file
    last_timestamp = df['Timestamp'].iloc[-1]

    # Get the user ID and username from the file name
    user_id = os.path.basename(file_path).split('_')[0]
    id_names = pd.read_csv('../data/congress_id_names.csv')
    username = id_names.loc[id_names['Id'] == int(user_id), 'Username'].values[0]

    # Scrape the tweets from the last timestamp to 2022-03-01
    num_tweets = scrape(
        scraper=scraper,
        query=f'(from:@{username}) until:{last_timestamp} since:2022-03-01',
        tweets=10,
        to_csv=False
    )

    # If the scraper returns tweets, delete the file
    if num_tweets > 0:
        os.remove(file_path)
        print(f"[{current_index}/{total_files}] Deleted {file_path} due to new tweets found after the last timestamp.")
        return False

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
    for index, filename in enumerate(files[::-1], start=1):
        file_path = os.path.join(directory, filename)
        process_file(file_path, index, total_files, scraper)


load_dotenv()
main()
