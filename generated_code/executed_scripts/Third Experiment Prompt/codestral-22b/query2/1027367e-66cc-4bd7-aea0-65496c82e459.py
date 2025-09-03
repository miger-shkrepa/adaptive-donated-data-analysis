import json
import os
import csv

# Define the root directory
root_dir = "root_dir"

# Initialize an empty dictionary to store the results
results = {}

# Define the paths to the JSON files
liked_posts_path = os.path.join(root_dir, "your_instagram_activity", "likes", "liked_posts.json")
saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")

# Function to process a JSON file
def process_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"FileNotFoundError: The file {file_path} does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"ValueError: The file {file_path} is not a valid JSON file.")

    for post in data:
        title = post.get("title", "")
        if title:
            company_name = title.split(" ")[0]  # Assuming the company name is the first word in the title
            if company_name in results:
                results[company_name] += 1
            else:
                results[company_name] = 1

# Process the JSON files
try:
    process_json_file(liked_posts_path)
    process_json_file(saved_posts_path)
except Exception as e:
    print(e)

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    for company, count in results.items():
        writer.writerow([company, count])