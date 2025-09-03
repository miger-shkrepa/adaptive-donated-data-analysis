import os
import csv

root_dir = "root_dir"

if not os.path.exists(root_dir):
    raise FileNotFoundError("Error: The root directory does not exist.")

following_path = os.path.join(root_dir, "personal_information", "following.json")
follow_requests_path = os.path.join(root_dir, "personal_information", "follow_requests_you've_received.json")

following = set()
follow_requests = set()

try:
    with open(following_path, 'r') as file:
        data = json.load(file)
        for item in data["relationships_following"]:
            following.add(item["string_list_data"][0]["value"])
except FileNotFoundError:
    print("Warning: The following.json file does not exist.")

try:
    with open(follow_requests_path, 'r') as file:
        data = json.load(file)
        for item in data["relationships_follow_requests_received"]:
            follow_requests.add(item["string_list_data"][0]["value"])
except FileNotFoundError:
    print("Warning: The follow_requests_you've_received.json file does not exist.")

not_following_back = following - follow_requests

with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Profile"])
    for profile in not_following_back:
        writer.writerow([profile])