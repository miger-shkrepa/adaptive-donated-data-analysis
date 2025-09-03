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

    # Iterate through the files and extract company names
    for file_path in files_to_check:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                # Extract company names from the JSON data
                # This is a placeholder for the actual extraction logic
                # You would need to implement the specific logic to extract company names from each JSON file
                # For example, you might look for specific keys or patterns in the JSON data
                # company_names.update(extract_company_names_from_json(data))
        except FileNotFoundError:
            # If the file is not found, continue with the next file
            continue
        except json.JSONDecodeError:
            # If the file is not a valid JSON, continue with the next file
            continue

    return company_names

# Function to write the company names to a CSV file
def write_company_names_to_csv(company_names, output_csv):
    try:
        with open(output_csv, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Company Name'])
            for company in company_names:
                writer.writerow([company])
    except Exception as e:
        raise IOError(f"Error: {str(e)}")

# Main function to execute the script
def main():
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

    company_names = extract_company_names(root_dir)

    if not company_names:
        # If no company names are found, write only the column headers to the CSV file
        write_company_names_to_csv([], output_csv)
    else:
        write_company_names_to_csv(company_names, output_csv)

if __name__ == "__main__":
    main()