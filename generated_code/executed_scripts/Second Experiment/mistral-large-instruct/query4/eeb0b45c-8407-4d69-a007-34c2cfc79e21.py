import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Function to extract company names from the directory structure
def extract_company_names(root_dir):
    company_names = set()

    # Define the paths to the relevant JSON files
    files_to_check = [
        os.path.join(root_dir, 'your_instagram_activity', 'comments', 'reels_comments.json'),
        os.path.join(root_dir, 'your_instagram_activity', 'likes', 'liked_posts.json'),
        os.path.join(root_dir, 'your_instagram_activity', 'events', 'event_reminders.json'),
        os.path.join(root_dir, 'personal_information', 'instagram_profile_information.json'),
        os.path.join(root_dir, 'personal_information', 'note_interactions.json'),
        os.path.join(root_dir, 'personal_information', 'personal_information.json'),
        os.path.join(root_dir, 'information_about_you', 'locations_of_interest.json'),
        os.path.join(root_dir, 'information_about_you', 'profile_based_in.json'),
        os.path.join(root_dir, 'devices.json')
    ]

    for file_path in files_to_check:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                # Extract company names from the JSON data
                company_names.update(extract_from_json(data))
        except FileNotFoundError:
            # If the file is not found, continue with the next file
            continue
        except json.JSONDecodeError:
            raise ValueError(f"Error: Invalid JSON format in file {file_path}.")

    return company_names

# Function to extract company names from JSON data
def extract_from_json(data):
    company_names = set()
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "string_map_data":
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, dict) and "value" in sub_value:
                        company_names.add(sub_value["value"])
            company_names.update(extract_from_json(value))
    elif isinstance(data, list):
        for item in data:
            company_names.update(extract_from_json(item))
    return company_names

# Main function to generate the CSV file
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("Error: The root directory does not exist.")

    company_names = extract_company_names(root_dir)

    # Write the company names to the CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Company Name"])
        for name in company_names:
            writer.writerow([name])

if __name__ == "__main__":
    main()