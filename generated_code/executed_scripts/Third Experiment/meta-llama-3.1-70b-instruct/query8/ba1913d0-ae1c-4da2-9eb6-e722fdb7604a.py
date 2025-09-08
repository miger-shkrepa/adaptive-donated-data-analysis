import os
import json
import csv

root_dir = "root_dir"

def get_interactions(root_dir):
    interactions = {}
    try:
        # Check if root directory exists
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

        # Iterate over all files in the directory
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for filename in filenames:
                if filename.endswith(".json"):
                    file_path = os.path.join(dirpath, filename)
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        if 'story_activities_story_likes' in data:
                            for item in data['story_activities_story_likes']:
                                title = item['title']
                                if title not in interactions:
                                    interactions[title] = {'post_likes': 0, 'story_likes': 0, 'comments': 0}
                                interactions[title]['story_likes'] += len(item['string_list_data'])
                        elif 'story_activities_countdowns' in data:
                            for item in data['story_activities_countdowns']:
                                title = item['title']
                                if title not in interactions:
                                    interactions[title] = {'post_likes': 0, 'story_likes': 0, 'comments': 0}
                                interactions[title]['comments'] += len(item['string_list_data'])
                        elif 'subscriptions_reels' in data:
                            for item in data['subscriptions_reels']:
                                title = item['title']
                                if title not in interactions:
                                    interactions[title] = {'post_likes': 0, 'story_likes': 0, 'comments': 0}
                                interactions[title]['post_likes'] += 1
    except Exception as e:
        raise ValueError("Error: " + str(e))

    return interactions

def write_to_csv(interactions):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])
            sorted_interactions = sorted(interactions.items(), key=lambda x: x[1]['post_likes'] + x[1]['story_likes'] + x[1]['comments'], reverse=True)
            for user, interaction in sorted_interactions[:20]:
                writer.writerow([user, interaction['post_likes'], interaction['story_likes'], interaction['comments']])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        interactions = get_interactions(root_dir)
        write_to_csv(interactions)
    except Exception as e:
        print("Error: " + str(e))
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["User", "Post Likes", "Story Likes", "Comments"])

if __name__ == "__main__":
    main()