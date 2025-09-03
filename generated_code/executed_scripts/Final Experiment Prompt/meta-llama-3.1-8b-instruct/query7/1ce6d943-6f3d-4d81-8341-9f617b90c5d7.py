import csv
import json
import os

root_dir = "root_dir"

try:
    root_dir = os.path.abspath(root_dir)
    if not os.path.exists(root_dir):
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
except Exception as e:
    raise ValueError("Error: " + str(e))

story_interactions_dir = os.path.join(root_dir, "your_instagram_activity", "story_interactions")

if not os.path.exists(story_interactions_dir):
    print("Warning: story_interactions directory does not exist. Returning CSV with only column headers.")
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["User", "Times Engaged"])
    exit()

results = {}

for filename in os.listdir(story_interactions_dir):
    if filename.endswith(".json"):
        filepath = os.path.join(story_interactions_dir, filename)
        try:
            with open(filepath, 'r') as json_file:
                data = json.load(json_file)
                for section in data:
                    if isinstance(section, dict):  # Check if section is a dictionary
                        title = section.get("title", "")
                        string_list_data = section.get("string_list_data", [])
                        times_engaged = len(string_list_data)
                        user = title
                        results[user] = results.get(user, 0) + times_engaged
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON in file {filename}: {e}")

with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["User", "Times Engaged"])
    for user, times_engaged in sorted(results.items(), key=lambda x: x[1], reverse=True):
        writer.writerow([user, times_engaged])