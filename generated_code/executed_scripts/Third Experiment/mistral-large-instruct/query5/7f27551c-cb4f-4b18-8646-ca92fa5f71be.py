import os
import json
import csv
from datetime import datetime

root_dir = "root_dir"

def extract_login_data(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("Error: The root directory does not exist.")

        # Define the path to the saved_posts.json file
        saved_posts_path = os.path.join(root_dir, "your_instagram_activity", "saved", "saved_posts.json")

        # Check if the saved_posts.json file exists
        if not os.path.exists(saved_posts_path):
            raise FileNotFoundError("Error: The saved_posts.json file does not exist.")

        # Read the saved_posts.json file
        with open(saved_posts_path, 'r') as file:
            saved_posts_data = json.load(file)

        # Extract login data
        login_data = []
        for item in saved_posts_data.get("saved_saved_media", []):
            string_map_data = item.get("string_map_data", {})
            saved_on = string_map_data.get("Saved on", {})
            href = saved_on.get("href")
            timestamp = saved_on.get("timestamp")
            if href and timestamp:
                login_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
                login_data.append((href, login_time))

        # Write the login data to a CSV file
        output_path = 'query_responses/results.csv'
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Device ID", "Login Time"])
            csvwriter.writerows(login_data)

    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except ValueError as val_error:
        print(f"Error: {val_error}")
    except Exception as e:
        print(f"Error: {e}")

# Call the function to extract login data
extract_login_data(root_dir)