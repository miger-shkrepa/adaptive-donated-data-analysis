import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to count story engagements
def count_story_engagements(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store engagement counts
        engagement_counts = {}

        # Walk through the directory structure
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith(".json"):
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r') as file:
                        try:
                            data = json.load(file)
                            # Check if the file contains story engagement data
                            if "story_engagements" in data:
                                for engagement in data["story_engagements"]:
                                    user = engagement.get("user")
                                    if user:
                                        if user in engagement_counts:
                                            engagement_counts[user] += 1
                                        else:
                                            engagement_counts[user] = 1
                        except json.JSONDecodeError:
                            raise ValueError("ValueError: Failed to decode JSON file.")

        # Prepare the CSV output
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for user, count in engagement_counts.items():
                writer.writerow({'User': user, 'Times Engaged': count})

    except Exception as e:
        raise e

# Run the function
count_story_engagements(root_dir)