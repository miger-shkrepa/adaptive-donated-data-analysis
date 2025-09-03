import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the topics of interest
topics_of_interest = []

# Define the path to the recommended_topics.json file
recommended_topics_path = os.path.join(root_dir, "preferences", "your_topics", "recommended_topics.json")

# Check if the recommended_topics.json file exists
if os.path.exists(recommended_topics_path):
    # Load the JSON data from the file
    with open(recommended_topics_path, 'r') as file:
        data = json.load(file)

    # Extract the topics of interest from the JSON data
    for topic in data["topics_your_topics"]:
        if "string_map_data" in topic and "Name" in topic["string_map_data"]:
            topics_of_interest.append(topic["string_map_data"]["Name"]["value"])

# Define the path to save the results.csv file
results_path = "query_responses/results.csv"

# Create the directory if it does not exist
os.makedirs(os.path.dirname(results_path), exist_ok=True)

# Write the topics of interest to a CSV file
with open(results_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Topics of Interest"])
    writer.writerows([[topic] for topic in topics_of_interest])