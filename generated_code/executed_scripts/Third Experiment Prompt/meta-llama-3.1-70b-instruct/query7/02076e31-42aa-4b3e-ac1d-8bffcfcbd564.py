import os
import json
import csv

root_dir = "root_dir"

def get_story_engagements(root_dir):
    story_engagements = {}
    try:
        for username in os.listdir(os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox')):
            if username != 'username_placeholder':
                for message_file in os.listdir(os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox', username)):
                    if message_file.endswith('.json'):
                        with open(os.path.join(root_dir, 'your_instagram_activity', 'messages', 'inbox', username, message_file), 'r') as f:
                            message_data = json.load(f)
                            for message in message_data['messages']:
                                if 'share' in message and 'original_content_owner' in message['share']:
                                    owner = message['share']['original_content_owner']
                                    if owner not in story_engagements:
                                        story_engagements[owner] = 1
                                    else:
                                        story_engagements[owner] += 1
    except FileNotFoundError:
        raise FileNotFoundError("Error: The root directory does not exist.")
    except Exception as e:
        raise ValueError("Error: " + str(e))
    return story_engagements

def write_csv(story_engagements):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['User', 'Times Engaged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, times_engaged in story_engagements.items():
            writer.writerow({'User': user, 'Times Engaged': times_engaged})

def main():
    story_engagements = get_story_engagements(root_dir)
    write_csv(story_engagements)

if __name__ == "__main__":
    main()