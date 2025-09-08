import os
import json
import csv

root_dir = "root_dir"
results = []

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Traverse the directory
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file == "posts_viewed.json":
            try:
                with open(os.path.join(root, file), 'r') as f:
                    data = json.load(f)
                    for item in data["impressions_history_posts_seen"]:
                        company = item["string_map_data"]["Author"]["value"]
                        results.append({"Company Name": company, "Number of Ads Viewed": 1})
            except FileNotFoundError:
                print(f"FileNotFoundError: The file {file} does not exist.")
            except json.JSONDecodeError:
                print(f"JSONDecodeError: The file {file} is not a valid JSON file.")

# Aggregate the results
aggregated_results = {}
for result in results:
    if result["Company Name"] in aggregated_results:
        aggregated_results[result["Company Name"]] += 1
    else:
        aggregated_results[result["Company Name"]] = 1

# Save the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    for company, count in aggregated_results.items():
        writer.writerow([company, count])