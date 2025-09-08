import os
import csv

root_dir = "root_dir"

def get_user_engagement(root_dir):
    try:
        # Check if the root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        user_engagement = {}

        # Check if the 'your_instagram_activity' directory exists
        your_instagram_activity_dir = os.path.join(root_dir, 'your_instagram_activity')
        if os.path.exists(your_instagram_activity_dir):
            # Check if the 'story_interactions' directory exists
            story_interactions_dir = os.path.join(your_instagram_activity_dir, 'story_interactions')
            if os.path.exists(story_interactions_dir):
                # Iterate over the story interaction files
                for filename in os.listdir(story_interactions_dir):
                    if filename.endswith('.json'):
                        # Open the JSON file and parse its content
                        filepath = os.path.join(story_interactions_dir, filename)
                        with open(filepath, 'r') as file:
                            # Since the JSON structure is not provided, we assume it's a list of dictionaries
                            # where each dictionary contains the user and the timestamp of engagement
                            try:
                                data = eval(file.read())
                                for item in data:
                                    if 'title' in item:
                                        user = item['title']
                                        if user not in user_engagement:
                                            user_engagement[user] = 1
                                        else:
                                            user_engagement[user] += 1
                            except Exception as e:
                                raise ValueError("ValueError: Failed to parse the JSON file: " + str(e))

        # Create the CSV file
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            if user_engagement:
                for user, times_engaged in user_engagement.items():
                    writer.writerow({'User': user, 'Times Engaged': times_engaged})
            else:
                # If no engagement data is found, write only the column headers
                pass

    except Exception as e:
        raise Exception("Error: " + str(e))

get_user_engagement(root_dir)