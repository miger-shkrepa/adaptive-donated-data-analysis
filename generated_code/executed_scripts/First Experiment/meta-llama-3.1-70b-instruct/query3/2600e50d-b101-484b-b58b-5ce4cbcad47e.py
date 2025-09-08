import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_posts_viewed(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store the posts viewed
        posts_viewed = {}

        # Iterate over the files in the root directory
        for filename in os.listdir(root_dir):
            # Check if the file is a JSON file
            if filename.endswith(".json"):
                # Open the JSON file
                with open(os.path.join(root_dir, filename), "r") as file:
                    # Load the JSON data
                    data = json.load(file)

                    # Check if the file contains posts viewed data
                    if "impressions_history_posts_seen" in data:
                        # Iterate over the posts viewed data
                        for post in data["impressions_history_posts_seen"]:
                            # Get the timestamp of the post
                            timestamp = post["string_map_data"]["Time"]["timestamp"]

                            # Convert the timestamp to a datetime object
                            date = datetime.fromtimestamp(timestamp)

                            # Get the date in the format YYYY-MM-DD
                            date_str = date.strftime("%Y-%m-%d")

                            # Check if the date is already in the posts_viewed dictionary
                            if date_str in posts_viewed:
                                # Increment the count of posts viewed for the date
                                posts_viewed[date_str]["Daily"] += 1
                            else:
                                # Add the date to the posts_viewed dictionary
                                posts_viewed[date_str] = {"Daily": 1, "Weekly": 0}

                            # Get the week of the year
                            week = date.isocalendar()[1]

                            # Get the week in the format Week YYYY-WW
                            week_str = f"Week {date.strftime('%Y-%U')}"

                            # Check if the week is already in the posts_viewed dictionary
                            if week_str in posts_viewed:
                                # Increment the count of posts viewed for the week
                                posts_viewed[week_str]["Weekly"] += 1
                            else:
                                # Add the week to the posts_viewed dictionary
                                posts_viewed[week_str] = {"Daily": 0, "Weekly": 1}

        # Return the posts_viewed dictionary
        return posts_viewed

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_to_csv(posts_viewed):
    try:
        # Open the CSV file
        with open("query_responses/results.csv", "w", newline="") as file:
            # Create a CSV writer
            writer = csv.writer(file)

            # Write the header
            writer.writerow(["Date/Week", "Posts Viewed", "Type"])

            # Iterate over the posts viewed data
            for date, data in posts_viewed.items():
                # Check if the date is a daily date
                if "Daily" in date:
                    # Write the daily data to the CSV file
                    writer.writerow([date, data["Daily"], "Daily"])
                # Check if the date is a weekly date
                elif "Week" in date:
                    # Write the weekly data to the CSV file
                    writer.writerow([date, data["Weekly"], "Weekly"])

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        # Get the posts viewed data
        posts_viewed = get_posts_viewed(root_dir)

        # Save the posts viewed data to a CSV file
        save_to_csv(posts_viewed)

    except Exception as e:
        print("Error: " + str(e))

if __name__ == "__main__":
    main()