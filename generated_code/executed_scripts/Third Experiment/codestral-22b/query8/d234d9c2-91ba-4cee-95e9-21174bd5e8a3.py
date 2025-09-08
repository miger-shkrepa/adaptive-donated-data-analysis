import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the interaction counts
interactions = {}

# Function to update the interaction counts
def update_interactions(username, count):
    if username in interactions:
        interactions[username] += count
    else:
        interactions[username] = count

# Process liked posts
liked_posts_path = os.path.join(root_dir, "likes", "liked_posts.json")
if os.path.exists(liked_posts_path):
    with open(liked_posts_path, "r") as f:
        liked_posts = json.load(f)
        for post in liked_posts["structure"]["likes_media_likes"]:
            for interaction in post["string_list_data"]:
                update_interactions(interaction["value"], 1)

# Process event reminders
event_reminders_path = os.path.join(root_dir, "events", "event_reminders.json")
if os.path.exists(event_reminders_path):
    with open(event_reminders_path, "r") as f:
        event_reminders = json.load(f)
        for reminder in event_reminders["structure"]["events_event_reminders"]:
            for interaction in reminder["string_list_data"]:
                update_interactions(interaction["value"], 1)

# Process note interactions
note_interactions_path = os.path.join(root_dir, "personal_information", "note_interactions.json")
if os.path.exists(note_interactions_path):
    with open(note_interactions_path, "r") as f:
        note_interactions = json.load(f)
        for interaction in note_interactions["structure"]["profile_note_interactions"][0]["string_map_data"]["Last Notes Seen Time"]:
            update_interactions(interaction["value"], 1)

# Sort the interactions dictionary by count in descending order
sorted_interactions = sorted(interactions.items(), key=lambda x: x[1], reverse=True)

# Get the top 20 interactions
top_interactions = sorted_interactions[:20]

# Write the results to a CSV file
with open("query_responses/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["User", "Interactions"])
    for user, count in top_interactions:
        writer.writerow([user, count])