import os
import json
import csv

root_dir = "root_dir"

def get_engagement_data(root_dir):
    engagement_data = {}
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Iterate through 'your_instagram_activity' directory
        activity_dir = os.path.join(root_dir, 'your_instagram_activity')
        if not os.path.exists(activity_dir):
            return engagement_data

        story_interactions_dir = os.path.join(activity_dir, 'story_interactions')
        if not os.path.exists(story_interactions_dir):
            return engagement_data

        # Iterate through story interactions files
        for filename in os.listdir(story_interactions_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(story_interactions_dir, filename)
                with open(filepath, 'r') as file:
                    data = json.load(file)
                    for interaction in data['story_activities_' + filename.split('.')[0]]:
                        user = interaction['title']
                        if user not in engagement_data:
                            engagement_data[user] = 0
                        engagement_data[user] += len(interaction['string_list_data'])

        # Iterate through 'messages' directory
        messages_dir = os.path.join(activity_dir, 'messages')
        if not os.path.exists(messages_dir):
            return engagement_data

        inbox_dir = os.path.join(messages_dir, 'inbox')
        if not os.path.exists(inbox_dir):
            return engagement_data

        # Iterate through inbox files
        for username in os.listdir(inbox_dir):
            filepath = os.path.join(inbox_dir, username, 'message_1.json')
            if os.path.exists(filepath):
                with open(filepath, 'r') as file:
                    data = json.load(file)
                    for message in data['messages']:
                        if 'share' in message and 'original_content_owner' in message['share']:
                            user = message['share']['original_content_owner']
                            if user not in engagement_data:
                                engagement_data[user] = 0
                            engagement_data[user] += 1

        return engagement_data

    except Exception as e:
        raise Exception("Error: " + str(e))

def write_to_csv(engagement_data):
    try:
        with open('query_responses/results.csv', 'w', newline='') as csvfile:
            fieldnames = ['User', 'Times Engaged']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user, times_engaged in engagement_data.items():
                writer.writerow({'User': user, 'Times Engaged': times_engaged})

    except Exception as e:
        raise Exception("Error: " + str(e))

def main():
    engagement_data = get_engagement_data(root_dir)
    write_to_csv(engagement_data)

if __name__ == "__main__":
    main()