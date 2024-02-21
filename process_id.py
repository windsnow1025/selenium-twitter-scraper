import os
import pandas as pd

# Read the id_names file once, as it will be used multiple times
id_names = pd.read_csv('data/congress_id_names.csv')

# Get the list of all files in the 'tweets' directory
tweet_files = os.listdir('tweets')

# Define the output folder
output_folder = "data/congress_tweets"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# Iterate over all tweet files
for filename in tweet_files:
    # Construct the full path of the file
    file_path = os.path.join('tweets', filename)

    # Read the CSV file
    tweets = pd.read_csv(file_path)

    # Check if the DataFrame is empty (only header row)
    if tweets.shape[0] <= 1:  # No data rows
        os.remove(file_path)  # Delete the file
        continue  # Skip the rest of the loop

    # Perform the conversion
    target_name = tweets['Handle'].iloc[0]
    target_without_at = target_name.replace('@', '')
    user_id = id_names.loc[id_names['Username'] == target_without_at, 'Id'].values[0]
    tweets['User ID'] = user_id

    # Construct the output file path
    output_filepath = os.path.join(output_folder, f"{user_id}_tweets.csv")

    # Check if the file already exists in the output directory
    if os.path.exists(output_filepath):
        # If it does, skip this iteration
        continue

    # Save the result to the output directory
    tweets.to_csv(output_filepath, index=False)
