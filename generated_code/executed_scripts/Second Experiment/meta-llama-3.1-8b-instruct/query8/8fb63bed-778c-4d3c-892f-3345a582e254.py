import csv
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the dictionary to store the user interactions
user_interactions = {}

# Iterate over the JSON files in the directory
for filename in os.listdir(root_dir):
    # Check if the file is a JSON file
    if filename.endswith(".json"):
        # Open the JSON file
        with open(os.path.join(root_dir, filename), 'r') as file:
            # Load the JSON data
            data = eval(file.read())

            # Iterate over the JSON data
            for key, value in data.items():
                # Check if the value is a dictionary
                if isinstance(value, dict):
                    # Check if the dictionary has a 'structure' key
                    if 'structure' in value:
                        # Iterate over the structure
                        for item in value['structure']:
                            # Check if the item is a list
                            if isinstance(item, list):
                                # Iterate over the list
                                for item2 in item:
                                    # Check if the item2 is a dictionary
                                    if isinstance(item2, dict):
                                        # Check if the dictionary has a 'string_list_data' key
                                        if 'string_list_data' in item2:
                                            # Iterate over the string_list_data
                                            for item3 in item2['string_list_data']:
                                                # Check if the item3 is a dictionary
                                                if isinstance(item3, dict):
                                                    # Check if the dictionary has a 'value' key
                                                    if 'value' in item3:
                                                        # Get the user and the interaction type
                                                        user = item2['title']
                                                        interaction_type = item3['value']

                                                        # Check if the user is already in the dictionary
                                                        if user in user_interactions:
                                                            # Increment the interaction count
                                                            user_interactions[user][interaction_type] += 1
                                                        else:
                                                            # Add the user to the dictionary with the interaction count
                                                            user_interactions[user] = {'Post Likes': 0, 'Story Likes': 0, 'Comments': 0}
                                                            user_interactions[user][interaction_type] += 1

# Sort the user interactions by the total interaction count
sorted_user_interactions = sorted(user_interactions.items(), key=lambda x: sum(x[1].values()), reverse=True)

# Write the sorted user interactions to a CSV file
with open('query_responses/results.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
    for user, interactions in sorted_user_interactions[:20]:
        writer.writerow([user, interactions['Post Likes'], interactions['Story Likes'], interactions['Comments']])