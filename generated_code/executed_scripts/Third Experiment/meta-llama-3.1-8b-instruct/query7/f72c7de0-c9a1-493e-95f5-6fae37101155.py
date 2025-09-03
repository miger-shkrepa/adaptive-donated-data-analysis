import csv
import os

def get_story_interactions(root_dir):
    story_interactions = []
    for filename in os.listdir(root_dir):
        file_path = os.path.join(root_dir, filename)
        if os.path.isfile(file_path):
            if filename.endswith(".json"):
                with open(file_path, 'r') as f:
                    data = eval(f.read())
                    if 'story_interactions' in data and 'story_likes.json' in data['story_interactions']:
                        story_likes = data['story_interactions']['story_likes.json']
                        for story in story_likes['structure']['story_activities_story_likes']:
                            story_interactions.append({
                                'user': story['title'],
                                'times_engaged': len(story['string_list_data'])
                            })
    return story_interactions

def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['User', 'Times Engaged']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    root_dir = "root_dir"
    try:
        story_interactions = get_story_interactions(root_dir)
        write_to_csv(story_interactions, 'query_responses/results.csv')
    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except Exception as e:
        raise ValueError("ValueError: An error occurred while processing the data.")

if __name__ == "__main__":
    main()