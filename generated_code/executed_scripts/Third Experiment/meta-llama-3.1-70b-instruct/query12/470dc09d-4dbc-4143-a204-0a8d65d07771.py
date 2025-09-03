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

        # Iterate over each subfolder in the root directory
        for subfolder in os.listdir(root_dir):
            subfolder_path = os.path.join(root_dir, subfolder)

            # Check if the subfolder is a directory
            if os.path.isdir(subfolder_path):
                # Iterate over each file in the subfolder
                for filename in os.listdir(subfolder_path):
                    # Check if the file is a JSON file
                    if filename.startswith("message_") and filename.endswith(".json"):
                        file_path = os.path.join(subfolder_path, filename)

                        # Open and read the JSON file
                        with open(file_path, "r") as file:
                            data = json.load(file)

                            # Iterate over each message in the JSON file
                            for message in data["messages"]:
                                # Get the timestamp of the message
                                timestamp_ms = message["timestamp_ms"]

                                # Convert the timestamp to a datetime object
                                dt = datetime.fromtimestamp(timestamp_ms / 1000)

                                # Get the week of the year
                                week = dt.strftime("Week %Y-%U")

                                # Increment the messages sent for the week
                                if week in messages_sent_per_week:
                                    messages_sent_per_week[week] += 1
                                else:
                                    messages_sent_per_week[week] = 1

        # Create a list of tuples to store the results
        results = [(week, messages_sent) for week, messages_sent in messages_sent_per_week.items()]

        # Sort the results by week
        results.sort(key=lambda x: x[0])

        return results

    except Exception as e:
        raise ValueError("Error: " + str(e))

def save_results_to_csv(results):
    try:
        # Create the results directory if it does not exist
        results_dir = "query_responses"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        # Save the results to a CSV file
        with open(os.path.join(results_dir, "results.csv"), "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Week", "Messages Sent"])
            writer.writerows(results)

    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        results = get_messages_sent_per_week(root_dir)
        save_results_to_csv(results)
    except Exception as e:
        print("Error: " + str(e))
        # Save an empty CSV file if an error occurs
        with open("query_responses/results.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Week", "Messages Sent"])

if __name__ == "__main__":
    main()