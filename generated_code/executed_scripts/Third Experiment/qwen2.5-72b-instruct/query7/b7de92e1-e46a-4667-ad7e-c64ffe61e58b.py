import os
import json
import csv

root_dir = "root_dir"

def get_user_engagement_with_stories(root_dir):
    user_engagement = {}
    stories_path = os.path.join(root_dir, "media", "stories")

    if not os.path.exists(stories_path):
        raise FileNotFoundError("FileNotFoundError: The stories directory does not exist.")
    
    try:
        for year_month in os.listdir(stories_path):
            year_month_path = os.path.join(stories_path, year_month)
            if os.path.isdir(year_month_path):
                for file_name in os.listdir(year_month_path):
                    file_path = os.path.join(year_month_path, file_name)
                    if file_name.endswith('.mp4') or file_name.endswith('.jpg'):
                        user = file_name.split('_')[0] if '_' in file_name else 'Unknown'
                        if user in user_engagement:
                            user_engagement[user] += 1
                        else:
                            user_engagement[user] = 1
    except Exception as e:
        raise ValueError(f"Error: Failed to process stories data - {str(e)}")

    return user_engagement

def write_to_csv(user_engagement):
    csv_path = 'query_responses/results.csv'
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    with open(csv_path, 'w', newline='') as csvfile:
        fieldnames = ['User', 'Times Engaged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, engagement in user_engagement.items():
            writer.writerow({'User': user, 'Times Engaged': engagement})

try:
    user_engagement = get_user_engagement_with_stories(root_dir)
    write_to_csv(user_engagement)
except FileNotFoundError as e:
    print(e)
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['User', 'Times Engaged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
except ValueError as e:
    print(e)
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['User', 'Times Engaged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()