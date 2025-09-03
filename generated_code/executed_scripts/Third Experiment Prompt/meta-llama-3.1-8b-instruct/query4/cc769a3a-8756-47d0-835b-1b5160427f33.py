import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the company names
company_names = []

# Iterate over the directory structure
for root, dirs, files in os.walk(root_dir):
    if "your_instagram_activity" in dirs:
        for subroot, subdirs, subfiles in os.walk(os.path.join(root_dir, "your_instagram_activity")):
            if "content" in subdirs:
                for filename in subfiles:
                    if filename.endswith(".json"):
                        filepath = os.path.join(subroot, filename)
                        try:
                            with open(filepath, 'r') as f:
                                data = json.load(f)
                                if "ig_archived_post_media" in data:
                                    company_names.append("Instagram")
                                elif "ig_profile_picture" in data:
                                    company_names.append("Instagram")
                                elif "ig_reels_media" in data:
                                    company_names.append("Instagram")
                                elif "ig_stories" in data:
                                    company_names.append("Instagram")
                        except json.JSONDecodeError:
                            print(f"Error: Failed to parse JSON file {filepath}")
                        except FileNotFoundError:
                            print(f"Error: File {filepath} not found")

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])
    writer.writerows([[company] for company in company_names])