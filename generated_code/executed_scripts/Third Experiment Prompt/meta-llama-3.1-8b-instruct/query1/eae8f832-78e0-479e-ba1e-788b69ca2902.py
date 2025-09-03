import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the topics of interest
topics_of_interest = []

# Iterate over the directory structure
for root, dirs, files in os.walk(root_dir):
    if "your_topics" in dirs:
        for filename in files:
            if filename.endswith(".txt"):
                topics_of_interest.append("No data available")
            elif filename.endswith(".json"):
                try:
                    file_path = os.path.join(root, filename)
                    with open(file_path, 'r') as file:
                        data = file.read()
                        if "topics" in data:
                            topics_of_interest.append("Topics available")
                        else:
                            topics_of_interest.append("No topics available")
                except Exception as e:
                    topics_of_interest.append("Error: " + str(e))

# Write the topics of interest to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Topics of Interest"])
    writer.writerows([topic] for topic in topics_of_interest)