import pandas as pd

# Path to the CSV file
file_path = '../data/congress_id_names.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Replace "BHigginsBflo" with "Bhigginsbflo"
df.replace("Bhigginsbflo", "BHigginsBflo", inplace=True)

# Write the modified DataFrame back to the file
df.to_csv(file_path, index=False)

print("The data has been updated.")
