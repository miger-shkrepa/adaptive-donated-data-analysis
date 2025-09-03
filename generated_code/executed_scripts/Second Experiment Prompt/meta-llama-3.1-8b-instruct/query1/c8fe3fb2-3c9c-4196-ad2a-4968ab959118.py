import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list of topics of interest
topics_of_interest = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as f:
            # Load the JSON data
            data = json.load(f)
            
            # Check if the JSON data has a 'topics_your_topics' key
            if 'topics_your_topics' in data:
                # Iterate over the topics of interest
                for topic in data['topics_your_topics']:
                    # Add the topic to the list of topics of interest
                    topics_of_interest.append(topic['Name'])

# Write the topics of interest to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Topics of Interest"])
    writer.writerows([topic for topic in topics_of_interest])

print("Query complete. Results saved to query_responses/results.csv")