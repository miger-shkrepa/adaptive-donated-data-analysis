import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the data structures
user_interactions = {}

# Iterate over the JSON files in the directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Check if the JSON file contains the required data
            if "relationships_follow_requests_sent" in data:
                # Iterate over the relationships in the JSON file
                for relationship in data["relationships_follow_requests_sent"]:
                    # Get the user and the interaction type
                    user = relationship["title"]
                    interaction_type = "Post Likes"

                    # Update the user interactions
                    if user in user_interactions:
                        user_interactions[user][interaction_type] += 1
                    else:
                        user_interactions[user] = {interaction_type: 1}

            elif "relationships_permanent_follow_requests" in data:
                # Iterate over the relationships in the JSON file
                for relationship in data["relationships_permanent_follow_requests"]:
                    # Get the user and the interaction type
                    user = relationship["title"]
                    interaction_type = "Story Likes"

                    # Update the user interactions
                    if user in user_interactions:
                        user_interactions[user][interaction_type] += 1
                    else:
                        user_interactions[user] = {interaction_type: 1}

            elif "profile_note_interactions" in data:
                # Iterate over the relationships in the JSON file
                for relationship in data["profile_note_interactions"]:
                    # Get the user and the interaction type
                    user = relationship["title"]
                    interaction_type = "Comments"

                    # Update the user interactions
                    if user in user_interactions:
                        user_interactions[user][interaction_type] += 1
                    else:
                        user_interactions[user] = {interaction_type: 1}

# Sort the user interactions by the total number of interactions
sorted_user_interactions = sorted(user_interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)

# Write the sorted user interactions to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the column headers
    writer.writeheader()

    # Write the user interactions
    for user, interactions in sorted_user_interactions:
        writer.writerow({'User': user, 'Post Likes': interactions.get('Post Likes', 0), 'Story Likes': interactions.get('Story Likes', 0), 'Comments': interactions.get('Comments', 0)})

        # Limit the output to the top 20 users
        if len(sorted_user_interactions) > 20:
            break