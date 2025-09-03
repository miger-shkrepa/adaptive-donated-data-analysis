import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list to store topics of interest
topics_of_interest = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = file.read()
            # Parse the JSON data
            json_data = eval(data)
            # Check if the JSON data contains the 'your_topics' key
            if 'your_topics' in json_data:
                # Iterate over the topics
                for topic in json_data['your_topics']['recommended_topics.json']['structure']['topics_your_topics']:
                    # Extract the topic name
                    topic_name = topic['string_map_data']['Name']['value']
                    # Add the topic name to the list
                    topics_of_interest.append(topic_name)

# Create the CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    # Create the CSV writer
    writer = csv.writer(csvfile)
    # Write the column headers
    writer.writerow(['Topics of Interest'])
    # Write the topics of interest
    writer.writerows([[topic] for topic in topics_of_interest])