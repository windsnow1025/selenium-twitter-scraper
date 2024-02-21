import os

import pandas as pd
from dotenv import load_dotenv

from scraper.scraper import scrape, signin

df = pd.read_csv('data/congress_id_names.csv')
usernames = df['Username'].tolist()

load_dotenv()
username = os.environ.get("TWITTER_USERNAME")
password = os.environ.get("TWITTER_PASSWORD")

scraper = signin(username=username, password=password)
try:
    for username in usernames:
        scrape(
            scraper=scraper,
            query=f'(from:@{username}) until:2022-06-09 since:2022-03-01',
            tweets=999
        )
except Exception:
    scraper.driver.close()
