import pandas as pd

from scraper.__main__ import main

df = pd.read_csv('data/congress_id_names.csv')
usernames = df['Username'].tolist()

for username in usernames:
    main(query=f'(from:@{username}) until:2022-06-09 since:2022-03-01', tweets=9999)
