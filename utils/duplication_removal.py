import os
import pandas as pd


def remove_duplicate_timestamps(file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Drop duplicates based on the 'Timestamp' column, keeping the first occurrence
    df_cleaned = df.drop_duplicates(subset=['Timestamp'], keep='first')

    # Save the cleaned DataFrame back to the file, overwriting the original
    df_cleaned.to_csv(file_path, index=False)


def remove_duplications():
    directory = "data/congress_tweets/"
    files = os.listdir(directory)

    # Process each file
    for filename in files:
        file_path = os.path.join(directory, filename)
        remove_duplicate_timestamps(file_path)

    print("Duplications removed.")
