import os
import json
import csv

root_dir = "root_dir"
output_file = "query_responses/results.csv"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the results
results = []

# Traverse the directory
for dirpath, dirnames, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename == "posts_viewed.json":
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    for item in data["impressions_history_posts_seen"]:
                        company_name = item["string_map_data"]["Author"]["value"]
                        results.append({"Company Name": company_name, "Number of Ads Viewed": 1})
            except FileNotFoundError:
                print(f"FileNotFoundError: The file {filepath} does not exist.")
            except json.JSONDecodeError:
                print(f"JSONDecodeError: The file {filepath} is not a valid JSON file.")

# Aggregate the results
aggregated_results = {}
for result in results:
    company_name = result["Company Name"]
    if company_name in aggregated_results:
        aggregated_results[company_name] += 1
    else:
        aggregated_results[company_name] = 1

# Write the results to a CSV file
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    for company_name, count in aggregated_results.items():
        writer.writerow([company_name, count])