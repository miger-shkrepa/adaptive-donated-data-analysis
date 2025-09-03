import csv
import json
import os

# Set the root directory to the main folder
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Set the path to the recommended topics file
recommended_topics_file = os.path.join(root_dir, "preferences", "your_topics", "recommended_topics.json")

# Check if the recommended topics file exists
if not os.path.exists(recommended_topics_file):
    print("Warning: Recommended topics file does not exist. Returning CSV file with only column headers.")
else:
    try:
        # Load the recommended topics data from JSON
        with open(recommended_topics_file, 'r') as f:
            recommended_topics_data = json.load(f)

        # Extract the 'Topics of Interest' from each entry in topics_your_topics
        topics_of_interest = [entry['string_map_data']['Name']['value'] for entry in recommended_topics_data['topics_your_topics']]

        # Write the 'Topics of Interest' to a CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Topics of Interest'])  # Write column headers
            writer.writerows([[topic] for topic in topics_of_interest])  # Write data

        print("CSV file written to query_responses/results.csv")

    except json.JSONDecodeError as e:
        raise ValueError("Error: Failed to parse JSON in recommended topics file: " + str(e))
    except Exception as e:
        raise ValueError("Error: An unexpected error occurred: " + str(e))