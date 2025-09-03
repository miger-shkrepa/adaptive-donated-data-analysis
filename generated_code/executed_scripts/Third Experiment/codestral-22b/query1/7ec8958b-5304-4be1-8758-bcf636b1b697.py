import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store topics of interest
topics_of_interest = []

# Define the path to the posts_viewed.json file
posts_viewed_file = os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json")

# Check if the posts_viewed.json file exists
if os.path.exists(posts_viewed_file):
    # Load the JSON data from the file
    with open(posts_viewed_file, "r") as f:
        data = json.load(f)

    # Extract the topics of interest from the JSON data
    for post in data["impressions_history_posts_seen"]:
        author = post["string_map_data"]["Author"]["value"]
        topics_of_interest.append(author)

# Define the path to the results.csv file
results_file = "query_responses/results.csv"

# Write the topics of interest to a CSV file
with open(results_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Topics of Interest"])
    writer.writerows([[topic] for topic in topics_of_interest])