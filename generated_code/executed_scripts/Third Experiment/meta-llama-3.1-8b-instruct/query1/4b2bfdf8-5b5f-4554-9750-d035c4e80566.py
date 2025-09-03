import csv
import os

# Declare the variable referring to the file input
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
            data = json.load(file)
            # Check if the JSON data contains the required structure
            if 'string_list_data' in data['structure']:
                # Extract the topics of interest from the JSON data
                topics_of_interest.extend([item['value'] for item in data['structure']['string_list_data']])

# Check if any topics of interest were found
if not topics_of_interest:
    # If not, return a CSV file with only the column headers
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Topics of Interest'])
else:
    # If topics of interest were found, write them to a CSV file
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Topics of Interest'])
        writer.writerows([[topic] for topic in topics_of_interest])

print("Query response saved to query_responses/results.csv")