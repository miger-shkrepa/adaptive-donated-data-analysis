import os
import json
import csv

root_dir = "root_dir"

def get_story_engagements(root_dir):
    story_engagements = {}
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Iterate through 'your_instagram_activity' directory
        activity_dir = os.path.join(root_dir, 'your_instagram_activity')
        if not os.path.exists(activity_dir):
            return story_engagements

        # Iterate through 'messages' directory
        messages_dir = os.path.join(activity_dir, 'messages')
        if not os.path.exists(messages_dir):
            return story_engagements

        # Iterate through 'inbox' directory
        inbox_dir = os.path.join(messages_dir, 'inbox')
        if not os.path.exists(inbox_dir):
            return story_engagements

        # Iterate through each conversation in 'inbox'
        for conversation in os.listdir(inbox_dir):
            conversation_dir = os.path.join(inbox_dir, conversation)
            if not os.path.exists(conversation_dir):
                continue

            # Iterate through each message in the conversation
            for message_file in os.listdir(conversation_dir):
                if not message_file.endswith('.json'):
                    continue

                message_path = os.path.join(conversation_dir, message_file)
                with open(message_path, 'r') as f:
                    message_data = json.load(f)

                # Check if the message is a story engagement
                if 'reactions' in message_data:
                    for reaction in message_data['reactions']:
                        user = reaction['actor']
                        if user not in story_engagements:
                            story_engagements[user] = 0
                        story_engagements[user] += 1

    except Exception as e:
        raise Exception(f"Error: {str(e)}")

    return story_engagements

def write_to_csv(story_engagements):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['User', 'Times Engaged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user, engagements in story_engagements.items():
            writer.writerow({'User': user, 'Times Engaged': engagements})

def main():
    story_engagements = get_story_engagements(root_dir)
    write_to_csv(story_engagements)

if __name__ == "__main__":
    main()