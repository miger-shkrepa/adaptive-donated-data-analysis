import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list of company names and ad counts
company_ads = []

# Iterate over the ads information directory
for company in os.listdir(os.path.join(root_dir, "ads_information")):
    if company == "ads_and_topics":
        # Iterate over the topics directory
        for topic in os.listdir(os.path.join(root_dir, "ads_information", "ads_and_topics")):
            if topic == "posts_viewed.json":
                # Load the JSON file
                with open(os.path.join(root_dir, "ads_information", "ads_and_topics", "posts_viewed.json"), "r") as f:
                    data = json.load(f)
                # Extract the impressions history posts seen
                impressions_history_posts_seen = data["impressions_history_posts_seen"]
                # Iterate over the impressions history posts seen
                for post in impressions_history_posts_seen:
                    # Extract the string map data
                    string_map_data = post["string_map_data"]
                    # Extract the author and time
                    author = string_map_data["Author"]["value"]
                    time = string_map_data["Time"]["timestamp"]
                    # Append the company name and ad count to the list
                    company_ads.append((author, 1))

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    for company, ad_count in company_ads:
        writer.writerow([company, ad_count])