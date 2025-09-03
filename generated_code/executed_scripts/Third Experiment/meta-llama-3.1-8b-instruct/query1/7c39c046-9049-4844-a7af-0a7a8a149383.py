import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the topics of interest
topics_of_interest = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON data contains the 'ads_and_topics' key
            if 'ads_and_topics' in data['ads_information']:
                # Iterate over the topics in the 'ads_and_topics' dictionary
                for topic, info in data['ads_information']['ads_and_topics'].items():
                    # Check if the topic is a JSON file
                    if info['type'] == 'json':
                        # Extract the topic of interest
                        topic_of_interest = topic.split('.')[0]

                        # Add the topic of interest to the list
                        topics_of_interest.append(topic_of_interest)

# Write the topics of interest to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Topics of Interest'])  # header
    writer.writerows([[topic] for topic in topics_of_interest])