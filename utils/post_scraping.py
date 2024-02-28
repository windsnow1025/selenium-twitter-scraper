import os

from utils.csv_transfer import csv_transfer
from utils.duplication_removal import remove_duplications


def post_scraping():
    try:
        # Process the scraped tweets
        csv_transfer()
        # Remove identical timestamps
        remove_duplications()
        # Remove the scraped tweets
        for filename in os.listdir('data/tweets'):
            os.remove(os.path.join('data/tweets', filename))
    except Exception as e:
        print(f"Error during processing: {e}")
