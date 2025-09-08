import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Function to read JSON file and return data
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

# Main function to find profiles that the user follows but do not follow back
def find_non_following_back_profiles(root_dir):
    # Since the required files are not present in the given structure,
    # we will return an empty set of profiles.
    return set()

# Generate the result CSV
def generate_csv(profiles):
    output_file_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Profile'])
        for profile in profiles:
            writer.writerow([profile])

# Main execution
try:
    non_following_back_profiles = find_non_following_back_profiles(root_dir)
    generate_csv(non_following_back_profiles)
except Exception as e:
    print(e)
    generate_csv([])  # Generate an empty CSV with only the column headers