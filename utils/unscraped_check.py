import os
import pandas as pd


def list_unscraped_usernames():
    # Load the ID and usernames mapping
    df = pd.read_csv('../data/congress_id_names.csv')

    # Define the output folder where scraped tweets are stored
    output_folder = "../data/congress_tweets"

    # Ensure the output folder exists to avoid errors when listing files
    if not os.path.exists(output_folder):
        print("No tweets have been scraped yet.")
        return

    # Get a list of already scraped user IDs by parsing filenames in the output folder
    already_scraped_filenames = os.listdir(output_folder)
    already_scraped_ids = [filename.split('_')[0] for filename in already_scraped_filenames]

    # Find all usernames that have not been scraped yet
    unscraped_usernames = df[~df['Id'].astype(str).isin(already_scraped_ids)]['Username'].tolist()

    if unscraped_usernames:
        print("Unscraped Twitter Usernames:")
        for username in unscraped_usernames:
            print(username)
    else:
        print("All usernames have been scraped.")


if __name__ == "__main__":
    list_unscraped_usernames()
