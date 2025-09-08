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

    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    # Define the path to the relevant JSON file
    story_engagement_file = os.path.join(root_dir, 'personal_information', 'instagram_profile_information.json')

    # Check if the file exists
    if not os.path.exists(story_engagement_file):
        return engagement_data

    # Read the JSON file
    try:
        with open(story_engagement_file, 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        raise ValueError("Error: The JSON file is not properly formatted.")

    # Extract story engagement data
    for entry in data.get('profile_account_insights', []):
        string_map_data = entry.get('string_map_data', {})
        for key, value in string_map_data.items():
            if 'Story Time' in key:
                user = value.get('value', 'Unknown')
                timestamp = value.get('timestamp', 0)
                if user not in engagement_data:
                    engagement_data[user] = 0
                engagement_data[user] += 1

    return engagement_data

# Function to write the engagement data to a CSV file
def write_engagement_to_csv(engagement_data, output_csv):
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['User', 'Times Engaged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user, times_engaged in engagement_data.items():
            writer.writerow({'User': user, 'Times Engaged': times_engaged})

# Main function to execute the script
def main():
    try:
        engagement_data = extract_story_engagement(root_dir)
        write_engagement_to_csv(engagement_data, output_csv)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()