import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def get_messages_sent_per_week(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Initialize a dictionary to store the messages sent per week
        messages_sent_per_week = {}

        # Iterate over the directories in the root directory
        for dir_name in os.listdir(root_dir):
            dir_path = os.path.join(root_dir, dir_name)

            # Check if the directory is a subdirectory
            if os.path.isdir(dir_path):
                # Iterate over the files in the subdirectory
                for file_name in os.listdir(dir_path):
                    file_path = os.path.join(dir_path, file_name)

                    # Check if the file is a JSON file
                    if file_name.startswith("message_") and file_name.endswith(".json"):
                        # Open the JSON file
                        with open(file_path, "r") as file:
                            # Load the JSON data
                            data = json.load(file)

                            # Iterate over the messages in the JSON data
                            for message in data.get("messages", []):
                                # Get the timestamp of the message
                                timestamp_ms = message.get("timestamp_ms")

                                # Check if the timestamp is valid
                                if timestamp_ms is not None:
                                    # Convert the timestamp to a datetime object
                                    dt = datetime.fromtimestamp(timestamp_ms / 1000)

                                    # Get the week of the year
                                    week = dt.strftime("%Y-W%U")

                                    # Increment the messages sent for the week
                                    messages_sent_per_week[week] = messages_sent_per_week.get(week, 0) + 1

        # Create a list of weeks and messages sent
        weeks = sorted(messages_sent_per_week.keys())
        messages_sent = [messages_sent_per_week.get(week, 0) for week in weeks]

        # Create a CSV file with the results
        with open("query_responses/results.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Week", "Messages Sent"])
            for week, messages in zip(weeks, messages_sent):
                writer.writerow([f"Week {week}", messages])

    except Exception as e:
        # Raise a ValueError with the error message
        raise ValueError(f"Error: {str(e)}")

get_messages_sent_per_week(root_dir)