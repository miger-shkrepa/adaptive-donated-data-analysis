import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the result list
result = []

# Iterate over the ads_and_topics directory
for file in os.listdir(os.path.join(root_dir, "ads_information", "ads_and_topics")):
    if file.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, "ads_information", "ads_and_topics", file), "r") as f:
            data = json.load(f)
        
        # Check if the 'structure' key exists in the JSON data
        if "structure" in data:
            # Extract the company name and number of ads viewed
            company_name = file.replace(".json", "")
            num_ads_viewed = len(data["structure"]["impressions_history_recs_hidden_authors"])
            
            # Append the result to the list
            result.append((company_name, num_ads_viewed))
        else:
            # If the 'structure' key does not exist, treat its contribution as 0
            result.append((file.replace(".json", ""), 0))

# Write the result to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    writer.writerows(result)