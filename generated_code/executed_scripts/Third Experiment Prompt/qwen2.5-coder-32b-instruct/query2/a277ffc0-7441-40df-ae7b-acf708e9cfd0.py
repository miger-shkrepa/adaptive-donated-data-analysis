import os
import csv
import json

# Define the root directory
root_dir = "root_dir"

# Define the path to the output CSV file
output_csv_path = 'query_responses/results.csv'

# Initialize a dictionary to store the count of ads viewed per company
ads_viewed_count = {}

# Function to process the posts_viewed.json file
def process_posts_viewed(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if 'impressions_history_posts_seen' in data:
                for entry in data['impressions_history_posts_seen']:
                    if 'string_map_data' in entry and 'Author' in entry['string_map_data']:
                        author = entry['string_map_data']['Author']['value']
                        if author in ads_viewed_count:
                            ads_viewed_count[author] += 1
                        else:
                            ads_viewed_count[author] = 1
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The posts_viewed.json file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The posts_viewed.json file is not a valid JSON file.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred while processing the posts_viewed.json file: {str(e)}")

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Construct the path to the posts_viewed.json file
posts_viewed_path = os.path.join(root_dir, 'ads_information', 'ads_and_topics', 'posts_viewed.json')

# Process the posts_viewed.json file if it exists
if os.path.exists(posts_viewed_path):
    process_posts_viewed(posts_viewed_path)

# Create the output directory if it does not exist
output_dir = os.path.dirname(output_csv_path)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Write the results to the CSV file
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Company Name', 'Number of Ads Viewed'])
    for company, count in ads_viewed_count.items():
        csvwriter.writerow([company, count])

print(f"Results have been saved to {output_csv_path}")