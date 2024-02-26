import os
import pandas as pd


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


def process_file(file_path, current_index, total_files):
    df = pd.read_csv(file_path)

    if should_delete_file(df):
        os.remove(file_path)
        print(
            f"[{current_index}/{total_files}] Deleted {file_path} due to it having a last timestamp after 2022-03-10 and at least 100 tweets.")
        return False

    if should_skip_file(df):
        print(f"[{current_index}/{total_files}] Skipped {file_path} based on skip conditions.")
        return False

    user_id = os.path.basename(file_path).split('_')[0]
    total_timestamps = df.shape[0]
    print(f"\n[{current_index}/{total_files}] File: {os.path.basename(file_path)}")
    print(f"User ID: {user_id}")
    print(f"First Timestamp: {df['Timestamp'].iloc[0]}")
    print(f"Last Timestamp: {df['Timestamp'].iloc[-1]}")
    print(f"Total Timestamps: {total_timestamps}")
    return True


def show_all_timestamps(file_path):
    df = pd.read_csv(file_path)
    print(df['Timestamp'] if not df.empty else "No timestamps available.")


def delete_file(file_path):
    os.remove(file_path)
    print(f"Deleted {file_path}")


def display_menu(file_path):
    while True:
        print("\nMenu:")
        print("1. Next file (Default)")
        print("2. Show all timestamps")
        print("3. Delete the file")
        choice = input("Enter your choice (Press Enter for Next file): ")

        if choice == '2':
            show_all_timestamps(file_path)
        elif choice == '3':
            delete_file(file_path)
            break
        else:
            break


def main():
    directory = "../data/congress_tweets/"
    files = os.listdir(directory)
    total_files = len(files)
    for index, filename in enumerate(files[::-1], start=1):
        file_path = os.path.join(directory, filename)
        if process_file(file_path, index, total_files):
            display_menu(file_path)
            if not os.path.exists(file_path):
                continue


if __name__ == "__main__":
    main()
