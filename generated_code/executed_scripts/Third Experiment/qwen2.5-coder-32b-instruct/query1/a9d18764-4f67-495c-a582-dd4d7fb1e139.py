import os
import csv

# Variable referring to the file input
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a list to store topics of interest
topics_of_interest = []

# Check for the presence of relevant files
recent_follow_requests_path = os.path.join(root_dir, "recent_follow_requests.json")
profile_photos_path = os.path.join(root_dir, "profile_photos.json")

# Since there is no direct data for topics of interest, we will just create a CSV with the header
# If there were data, we would parse the files and extract the topics here

# Define the output CSV file path
output_csv_path = 'query_responses/results.csv'

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

# Write the CSV file with the header
with open(output_csv_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Topics of Interest"])

print(f"CSV file with topics of interest has been created at {output_csv_path}")