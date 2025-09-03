import os
import csv
import datetime
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the output CSV file
output_file = "query_responses/results.csv"

# Initialize the CSV writer
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Date/Week", "Posts Viewed", "Type"])

    # Iterate over the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "posts_viewed.json":
                # Open the JSON file
                try:
                    with open(os.path.join(dirpath, filename), 'r') as json_file:
                        data = json.load(json_file)

                        # Extract the impressions history posts seen
                        impressions_history_posts_seen = data["impressions_history_posts_seen"]

                        # Iterate over the impressions history posts seen
                        for post in impressions_history_posts_seen:
                            # Extract the string map data
                            string_map_data = post["string_map_data"]

                            # Extract the time
                            time = string_map_data["Time"]["timestamp"]

                            # Convert the time to a date
                            date = datetime.datetime.fromtimestamp(time).strftime("%Y-%m-%d")

                            # Determine the type (daily or weekly)
                            if datetime.datetime.fromtimestamp(time).weekday() == 0:  # Monday
                                type = "Weekly"
                            else:
                                type = "Daily"

                            # Write the data to the CSV file
                            writer.writerow([date, len(impressions_history_posts_seen), type])
                except FileNotFoundError:
                    print(f"Error: The file '{os.path.join(dirpath, filename)}' does not exist.")
                except json.JSONDecodeError:
                    print(f"Error: The file '{os.path.join(dirpath, filename)}' is not a valid JSON file.")
                except KeyError:
                    print(f"Error: The file '{os.path.join(dirpath, filename)}' is missing required keys.")