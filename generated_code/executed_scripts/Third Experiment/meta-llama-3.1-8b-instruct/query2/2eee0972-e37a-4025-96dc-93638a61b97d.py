import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the list of company names and the number of ads viewed
company_names = []
num_ads_viewed = []

# Iterate over the ads and topics
for company, data in [
    ("ads_and_topics", {"posts_viewed.json": {"impressions_history_posts_seen": [{"string_map_data": {"Author": {"value": "str"}, "Time": {"timestamp": "int"}}}]}}),
    ("ads_and_topics", {"videos_watched.json": {"impressions_history_videos_watched": [{"string_map_data": {"Author": {"value": "str"}, "Time": {"timestamp": "int"}}}]}}),
    ("instagram_ads_and_businesses", {"subscription_for_no_ads.json": {"label_values": [{"label": "str", "value": "str"}]}})
]:
    # Check if the company exists
    if company not in root_dir:
        # If the company does not exist, treat its contribution as 0
        company_names.append(company)
        num_ads_viewed.append(0)
        continue

    # Initialize the number of ads viewed for the company
    num_ads_viewed_for_company = 0

    # Iterate over the posts viewed
    for file, data in data.items():
        # Check if the file exists
        if file not in root_dir:
            # If the file does not exist, treat its contribution as 0
            continue

        # Iterate over the impressions history posts seen
        for post in data["impressions_history_posts_seen"]:
            # Increment the number of ads viewed for the company
            num_ads_viewed_for_company += 1

    # Append the company name and the number of ads viewed to the lists
    company_names.append(company)
    num_ads_viewed.append(num_ads_viewed_for_company)

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name", "Number of Ads Viewed"])
    writer.writerows(zip(company_names, num_ads_viewed))