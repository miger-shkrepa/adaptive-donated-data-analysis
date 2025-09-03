import csv
import os
import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the lists to store the data
date_week = []
posts_viewed = []
type = []

# Iterate over the files in the root directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the file contains the required data
            if "ads_viewed.json" in filename:
                # Iterate over the impressions history ads seen
                for impression in data["ads_and_topics"]["ads_viewed.json"]["structure"]["impressions_history_ads_seen"]:
                    # Extract the date and time
                    date = impression["string_map_data"]["Time"]["timestamp"]
                    # Convert the date to the required format
                    if date < 7:
                        date_week.append(datetime.date.fromtimestamp(date).strftime("%Y-%m-%d"))
                        type.append("Daily")
                    else:
                        date_week.append(f"Week {datetime.date.fromtimestamp(date).strftime('%Y-%W')}")
                        type.append("Weekly")
                    # Increment the posts viewed count
                    posts_viewed.append(1)

            elif "posts_viewed.json" in filename:
                # Iterate over the impressions history posts seen
                for impression in data["ads_and_topics"]["posts_viewed.json"]["structure"]["impressions_history_posts_seen"]:
                    # Extract the date and time
                    date = impression["string_map_data"]["Time"]["timestamp"]
                    # Convert the date to the required format
                    if date < 7:
                        date_week.append(datetime.date.fromtimestamp(date).strftime("%Y-%m-%d"))
                        type.append("Daily")
                    else:
                        date_week.append(f"Week {datetime.date.fromtimestamp(date).strftime('%Y-%W')}")
                        type.append("Weekly")
                    # Increment the posts viewed count
                    posts_viewed.append(1)

# Write the data to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Date/Week", "Posts Viewed", "Type"])
    for i in range(len(date_week)):
        writer.writerow([date_week[i], posts_viewed[i], type[i]])