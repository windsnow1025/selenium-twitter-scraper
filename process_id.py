import os
import pandas as pd

filename = '2024-01-25_16-47-50_tweets_1-303.csv'

tweets = pd.read_csv(f'tweets/{filename}')
id_names = pd.read_csv('data/congress_id_names.csv')

target_name = tweets['Handle'].iloc[0]
target_without_at = target_name.replace('@', '')
user_id = id_names.loc[id_names['Username'] == target_without_at, 'Id'].values[0]

tweets['User ID'] = user_id

output_folder = "data/congress_tweet_data"
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

output_filepath = os.path.join(output_folder, f"{user_id}_tweets.csv")
tweets.to_csv(output_filepath, index=False)
