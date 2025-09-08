import csv
import os
import json

def get_user_interactions(root_dir):
    user_interactions = {}
    for filename in os.listdir(root_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(root_dir, filename)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if 'likes' in data and 'liked_posts.json' in data['likes']:
                        liked_posts = data['likes']['liked_posts.json']
                        for post in liked_posts['likes_media_likes']:
                            for interaction in post['string_list_data']:
                                user = interaction['value']
                                if user not in user_interactions:
                                    user_interactions[user] = {'post_likes': 0, 'story_likes': 0, 'comments': 0}
                                user_interactions[user]['post_likes'] += 1
                    elif 'personal_information' in data and 'personal_information.json' in data['personal_information']:
                        personal_info = data['personal_information']['personal_information.json']
                        for user in personal_info['profile_user']:
                            for interaction in user['string_map_data'].values():
                                if 'Post Likes' in interaction['value']:
                                    user_interactions[interaction['href']] = {'post_likes': int(interaction['value'].split(': ')[1]), 'story_likes': 0, 'comments': 0}
                                elif 'Story Likes' in interaction['value']:
                                    user_interactions[interaction['href']] = {'post_likes': 0, 'story_likes': int(interaction['value'].split(': ')[1]), 'comments': 0}
                                elif 'Comments' in interaction['value']:
                                    user_interactions[interaction['href']] = {'post_likes': 0, 'story_likes': 0, 'comments': int(interaction['value'].split(': ')[1])}
            except json.JSONDecodeError:
                raise ValueError("Error: Invalid JSON file: " + file_path)
    return user_interactions

def top_20_interactions(user_interactions):
    sorted_interactions = sorted(user_interactions.items(), key=lambda x: (x[1]['post_likes'] + x[1]['story_likes'] + x[1]['comments']), reverse=True)
    return sorted_interactions[:20]

def write_to_csv(sorted_interactions):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['User', 'Post Likes', 'Story Likes', 'Comments'])
        for user, interactions in sorted_interactions:
            writer.writerow([user, interactions['post_likes'], interactions['story_likes'], interactions['comments']])

def main():
    root_dir = "root_dir"
    try:
        user_interactions = get_user_interactions(root_dir)
        sorted_interactions = top_20_interactions(user_interactions)
        write_to_csv(sorted_interactions)
    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except ValueError as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()