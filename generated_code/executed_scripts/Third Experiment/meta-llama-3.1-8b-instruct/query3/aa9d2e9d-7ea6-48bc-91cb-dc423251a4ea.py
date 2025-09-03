import csv
import os
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the lists to store the data
date_week = []
posts_viewed = []
type = []

# Iterate over the 'ads_information' directory
ads_info_dir = os.path.join(root_dir, "ads_information")
if os.path.exists(ads_info_dir):
    for filename in os.listdir(ads_info_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(ads_info_dir, filename)
            with open(file_path, 'r') as f:
                data = json.load(f)
                if "ads_and_topics" in data:
                    for file in data["ads_and_topics"].values():
                        if file["type"] == "json":
                            if "impressions_history_posts_seen" in file["structure"]:
                                for item in file["structure"]["impressions_history_posts_seen"]:
                                    if "string_map_data" in item:
                                        for key, value in item["string_map_data"].items():
                                            if key == "Time":
                                                date = value["timestamp"]
                                                if date % 7 == 0:
                                                    date_week.append(f"Week {date // 7}-{date // 7 + 1}")
                                                    type.append("Weekly")
                                                else:
                                                    date_week.append(f"{date // 10000}-{(date // 100) % 100}-{date % 100}")
                                                    type.append("Daily")
                                                posts_viewed.append(1)
                                    else:
                                        posts_viewed.append(0)
else:
    print("Error: The 'ads_information' directory does not exist.")

# Write the data to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Date/Week", "Posts Viewed", "Type"])
    for i in range(len(date_week)):
        writer.writerow([date_week[i], posts_viewed[i], type[i]])