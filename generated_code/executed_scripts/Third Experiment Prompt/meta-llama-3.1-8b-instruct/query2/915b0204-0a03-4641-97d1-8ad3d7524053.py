import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list of company names and ad counts
company_names = []
ad_counts = []

# Iterate over the ads information directory
ads_info_dir = os.path.join(root_dir, "ads_information", "ads_and_topics")
if os.path.exists(ads_info_dir):
    # Iterate over the JSON files in the ads information directory
    for file in os.listdir(ads_info_dir):
        # Check if the file is a JSON file
        file_path = os.path.join(ads_info_dir, file)
        if file.endswith(".json"):
            try:
                # Load the JSON file
                with open(file_path, "r") as f:
                    data = json.load(f)
                # Extract the company name and ad count
                company_name = os.path.splitext(file)[0]
                ad_count = 0
                if "structure" in data and "impressions_history_ads_seen" in data["structure"]:
                    ad_count = len(data["structure"]["impressions_history_ads_seen"])
                # Append the company name and ad count to the lists
                company_names.append(company_name)
                ad_counts.append(ad_count)
            except json.JSONDecodeError:
                # If the JSON file is invalid, skip it
                print(f"Error: Invalid JSON file {file_path}")
            except KeyError:
                # If the JSON file does not contain the required data, skip it
                print(f"Error: Missing data in JSON file {file_path}")
else:
    # If the ads information directory does not exist, treat its contribution as 0
    company_names.append("ads_viewed")
    ad_counts.append(0)

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    for company, ad_count in zip(company_names, ad_counts):
        writer.writerow([company, ad_count])