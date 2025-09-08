import os
import json
import csv

# Declare the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize a dictionary to store the interaction counts
interaction_counts = {}

# Function to update the interaction counts from a JSON file
def update_interaction_counts(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for item in data:
                user = item['title']
                if user not in interaction_counts:
                    interaction_counts[user] = {'Post Likes': 0, 'Story Likes': 0, 'Comments': 0}
                if 'string_list_data' in item:
                    for interaction in item['string_list_data']:
                        if 'value' in interaction:
                            if 'liked_posts' in file_path:
                                interaction_counts[user]['Post Likes'] += 1
                            elif 'liked_comments' in file_path:
                                interaction_counts[user]['Comments'] += 1
                            elif 'stories' in file_path:
                                interaction_counts[user]['Story Likes'] += 1
    except FileNotFoundError:
        pass

# Update the interaction counts from the available JSON files
update_interaction_counts(os.path.join(root_dir, 'likes', 'liked_posts.json'))
update_interaction_counts(os.path.join(root_dir, 'likes', 'liked_comments.json'))
update_interaction_counts(os.path.join(root_dir, 'media', 'stories', '202311', 'image.jpg'))
update_interaction_counts(os.path.join(root_dir, 'media', 'stories', '202312', 'image.jpg'))

# Sort the interaction counts in descending order
sorted_interaction_counts = sorted(interaction_counts.items(), key=lambda x: sum(x[1].values()), reverse=True)

# Write the results to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
    for user, counts in sorted_interaction_counts[:20]:
        writer.writerow([user, counts['Post Likes'], counts['Story Likes'], counts['Comments']])