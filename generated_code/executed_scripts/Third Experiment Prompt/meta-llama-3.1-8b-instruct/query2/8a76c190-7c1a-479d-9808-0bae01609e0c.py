import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list of companies and their ad views
companies = []

# Iterate over the ads information directory
for company in os.listdir(os.path.join(root_dir, "ads_information", "ads_and_topics")):
    # Check if the company directory exists
    company_dir = os.path.join(root_dir, "ads_information", "ads_and_topics", company)
    if os.path.isdir(company_dir):
        # Iterate over the JSON files in the company directory
        for file in os.listdir(company_dir):
            # Check if the file is a JSON file
            if file.endswith(".json"):
                # Open the JSON file
                file_path = os.path.join(company_dir, file)
                try:
                    with open(file_path, "r") as f:
                        # Load the JSON data
                        data = json.load(f)
                        # Check if the JSON data has the expected structure
                        if "impressions_history_ads_seen" in data["structure"]:
                            # Iterate over the ad views
                            for ad_view in data["structure"]["impressions_history_ads_seen"]:
                                # Get the company name and ad view count
                                company_name = company
                                ad_view_count = len(ad_view["string_map_data"])
                                # Add the company and ad view count to the list
                                companies.append((company_name, ad_view_count))
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON file {file_path}: {e}")
                except FileNotFoundError as e:
                    print(f"Error opening file {file_path}: {e}")

# Write the companies and ad view counts to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    writer.writerows(companies)