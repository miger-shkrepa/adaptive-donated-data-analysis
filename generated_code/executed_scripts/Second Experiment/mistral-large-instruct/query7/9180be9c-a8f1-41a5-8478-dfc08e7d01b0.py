import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Initialize a dictionary to store engagement counts
engagement_counts = {}

# Function to process the directory and count story engagements
def process_directory(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Walk through the directory structure
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith(".json"):
                    file_path = os.path.join(dirpath, filename)
                    process_json_file(file_path)

        # Write the results to a CSV file
        write_csv(output_csv, engagement_counts)

    except Exception as e:
        print(f"Error: {e}")

# Function to process individual JSON files
def process_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            if "profile_account_insights" in data:
                for insight in data["profile_account_insights"]:
                    if "string_map_data" in insight:
                        string_map_data = insight["string_map_data"]
                        if "Last Story Time" in string_map_data:
                            user = string_map_data["Last Story Time"]["value"]
                            if user in engagement_counts:
                                engagement_counts[user] += 1
                            else:
                                engagement_counts[user] = 1

    except FileNotFoundError:
        print(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        print(f"ValueError: The file {file_path} is not a valid JSON file.")
    except Exception as e:
        print(f"Error: {e}")

# Function to write the results to a CSV file
def write_csv(output_csv, engagement_counts):
    try:
        with open(output_csv, 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for user, count in engagement_counts.items():
                writer.writerow({'User': user, 'Times Engaged': count})

    except Exception as e:
        print(f"Error: {e}")

# Execute the script
process_directory(root_dir)