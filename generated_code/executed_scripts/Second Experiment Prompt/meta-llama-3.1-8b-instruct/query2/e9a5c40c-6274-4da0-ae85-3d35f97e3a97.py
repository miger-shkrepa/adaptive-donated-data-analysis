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

# Iterate over the ads_information directory
for company in os.listdir(os.path.join(root_dir, "ads_information")):
    # Check if the company directory exists
    company_dir = os.path.join(root_dir, "ads_information", company)
    if not os.path.exists(company_dir):
        continue

    # Initialize the company result
    company_result = {"Company Name": company, "Number of Ads Viewed": 0}

    # Iterate over the ads_and_topics directory
    ads_and_topics_dir = os.path.join(company_dir, "ads_and_topics")
    if os.path.exists(ads_and_topics_dir):
        for topic in os.listdir(ads_and_topics_dir):
            # Check if the topic directory exists
            topic_dir = os.path.join(ads_and_topics_dir, topic)
            if not os.path.exists(topic_dir):
                continue

            # Load the topic JSON file
            try:
                with open(os.path.join(topic_dir, "ads_viewed.json"), "r") as f:
                    topic_data = json.load(f)
            except FileNotFoundError:
                # If the file does not exist, treat its contribution as 0
                continue

            # Extract the number of ads viewed
            if "structure" in topic_data and "impressions_history_ads_seen" in topic_data["structure"]:
                company_result["Number of Ads Viewed"] += len(topic_data["structure"]["impressions_history_ads_seen"])

    # Append the company result to the result list
    result.append(company_result)

# Write the result to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Company Name", "Number of Ads Viewed"])
    writer.writeheader()
    writer.writerows(result)