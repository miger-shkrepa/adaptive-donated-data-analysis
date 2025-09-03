import csv
import json
import os

# Define the root directory variable
root_dir = "root_dir"

try:
    # Check if the root directory exists
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
except FileNotFoundError as e:
    print(e)
    exit()

# Initialize the result list
results = []

# Iterate over the 'your_instagram_activity' directory
for activity in os.listdir(root_dir):
    if activity == "your_instagram_activity":
        # Iterate over the 'likes' and 'saved' directories
        for sub_activity in os.listdir(os.path.join(root_dir, activity)):
            if sub_activity in ["likes", "saved"]:
                # Initialize the company name and ad count variables
                company_name = ""
                ad_count = 0

                # Iterate over the JSON files in the sub-activity directory
                for file in os.listdir(os.path.join(root_dir, activity, sub_activity)):
                    if file.endswith(".json"):
                        # Open the JSON file and load its contents
                        with open(os.path.join(root_dir, activity, sub_activity, file), "r") as f:
                            data = json.load(f)

                        # Check if the JSON file has a 'structure' key
                        if "structure" in data:
                            # Extract the company name and ad count from the JSON data
                            if sub_activity == "likes":
                                for post in data["structure"]["likes_media_likes"]:
                                    for item in post.get("string_list_data", []):
                                        if item.get("value") == "ad":
                                            ad_count += 1
                            elif sub_activity == "saved":
                                for post in data["structure"]["saved_saved_media"]:
                                    for item in post.get("string_map_data", {}).values():
                                        if item.get("href") == "ad":
                                            ad_count += 1

                            # Update the company name and ad count variables
                            if company_name == "":
                                company_name = "Unknown"
                            results.append([company_name, ad_count])

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    writer.writerows(results)