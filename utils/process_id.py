import os
import pandas as pd


def process_id():
    # Read the id_names file once, as it will be used multiple times
    id_names = pd.read_csv('data/congress_id_names.csv')

    # Get the list of all files in the 'data/tweets' directory
    tweet_files = os.listdir('data/tweets')
    # Define the output folder
    output_folder = "data/congress_tweets"

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    # Iterate over all tweet files
    for filename in tweet_files:
        # Construct the full path of the file
        file_path = os.path.join('data/tweets', filename)

        # Read the CSV file
        tweets = pd.read_csv(file_path)

        # Check if the DataFrame is empty (only header row)
        if tweets.shape[0] == 0:  # No data rows
            os.remove(file_path)  # Delete the file
            continue  # Skip the rest of the loop

        # Perform the conversion
        target_name = tweets['Handle'].iloc[0]
        target_without_at = target_name.replace('@', '')
        filtered_ids = id_names.loc[id_names['Username'] == target_without_at, 'Id']

        if filtered_ids.empty:
            # If no matching user ID is found, raise an error
            raise ValueError(f"No matching user ID found for username '{target_without_at}' in file '{filename}'")

        user_id = filtered_ids.values[0]
        tweets['User ID'] = user_id

        # Construct the output file path
        output_filepath = os.path.join(output_folder, f"{user_id}_tweets.csv")

        # Save the result to the output directory
        if os.path.exists(output_filepath):
            # If the file exists, append without writing the header
            tweets.to_csv(output_filepath, mode='a', header=False, index=False)
        else:
            # If the file does not exist, create it and write the header
            tweets.to_csv(output_filepath, mode='w', header=True, index=False)

    print("Processing complete.")


if __name__ == "__main__":
    process_id()
