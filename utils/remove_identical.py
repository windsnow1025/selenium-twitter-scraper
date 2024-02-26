import os
import pandas as pd


def remove_duplicate_timestamps(file_path):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Drop duplicates based on the 'Timestamp' column, keeping the first occurrence
    df_cleaned = df.drop_duplicates(subset=['Timestamp'], keep='first')

    # Save the cleaned DataFrame back to the file, overwriting the original
    df_cleaned.to_csv(file_path, index=False)


def main():
    directory = "../data/congress_tweets/"

    # Ensure the directory exists
    if not os.path.exists(directory):
        print("Directory does not exist:", directory)
        return

    # List all CSV files in the directory
    files = [f for f in os.listdir(directory) if f.endswith('.csv')]

    # Process each file
    for filename in files:
        file_path = os.path.join(directory, filename)
        print(f"Processing {filename}...")
        remove_duplicate_timestamps(file_path)
        print(f"Processed {filename} successfully.")


if __name__ == "__main__":
    main()
