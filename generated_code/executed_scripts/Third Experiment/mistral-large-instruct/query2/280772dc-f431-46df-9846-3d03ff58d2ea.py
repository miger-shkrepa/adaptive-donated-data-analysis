import os
import json
import csv

# Define the root directory
root_dir = "root_dir"

# Define the output CSV file path
output_csv = 'query_responses/results.csv'

# Initialize a dictionary to store the results
results = {}

# Function to process the ads_viewed.json file
def process_ads_viewed(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for entry in data.get("impressions_history_ads_seen", []):
                author = entry.get("string_map_data", {}).get("Author", {}).get("value", "Unknown")
                if author not in results:
                    results[author] = 0
                results[author] += 1
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The ads_viewed.json file is not a valid JSON.")

# Function to process the directory structure
def process_directory(directory):
    ads_viewed_path = os.path.join(directory, "ads_information", "ads_and_topics", "ads_viewed.json")
    if os.path.exists(ads_viewed_path):
        process_ads_viewed(ads_viewed_path)
    else:
        # If the file does not exist, treat its contribution as 0
        pass

# Process the root directory
try:
    process_directory(root_dir)
except Exception as e:
    print(f"Error: {e}")

# Write the results to a CSV file
try:
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Company Name', 'Number of Ads Viewed']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for company, count in results.items():
            writer.writerow({'Company Name': company, 'Number of Ads Viewed': count})
except Exception as e:
    print(f"Error: {e}")