import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to extract story engagement data
def extract_story_engagement(root_dir):
    engagement_data = {}

    # Define the paths to the relevant JSON files
    story_files = [
        os.path.join(root_dir, 'story_interactions', 'polls.json'),
        os.path.join(root_dir, 'story_interactions', 'questions.json'),
        os.path.join(root_dir, 'story_interactions', 'quizzes.json'),
        os.path.join(root_dir, 'story_interactions', 'story_likes.json')
    ]

    # Process each story interaction file
    for file_path in story_files:
        if not os.path.exists(file_path):
            continue

        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
                for item in data.values():
                    for entry in item:
                        user = entry.get('title', 'Unknown')
                        timestamps = [int(ts.get('timestamp', 0)) for ts in entry.get('string_list_data', [])]
                        if user not in engagement_data:
                            engagement_data[user] = 0
                        engagement_data[user] += len(timestamps)
            except json.JSONDecodeError:
                raise ValueError(f"Error: Invalid JSON format in {file_path}")

    return engagement_data

# Function to write the results to a CSV file
def write_to_csv(engagement_data, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['User', 'Times Engaged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user, times_engaged in engagement_data.items():
            writer.writerow({'User': user, 'Times Engaged': times_engaged})

# Main function to execute the script
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    engagement_data = extract_story_engagement(root_dir)

    if not engagement_data:
        # Write only the column headers if no data is available
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    else:
        write_to_csv(engagement_data, output_csv)

if __name__ == "__main__":
    main()