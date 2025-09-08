import csv
import os

def get_user_interactions(root_dir):
    user_interactions = {}
    for filename in os.listdir(root_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(root_dir, filename)
            try:
                with open(file_path, 'r') as f:
                    data = eval(f.read())
                    if 'likes' in data and 'liked_posts.json' in data['likes']:
                        liked_posts = data['likes']['liked_posts.json']
                        for post in liked_posts['likes_media_likes']:
                            for interaction in post['string_list_data']:
                                user = interaction['value']
                                if user not in user_interactions:
                                    user_interactions[user] = {'post_likes': 0, 'story_likes': 0, 'comments': 0}
                                user_interactions[user]['post_likes'] += 1
                    if 'personal_information' in data and 'personal_information.json' in data['personal_information']:
                        personal_info = data['personal_information']['personal_information.json']
                        for user in personal_info['profile_user']:
                            for interaction in user['string_map_data'].values():
                                if 'Comments' in interaction['value']:
                                    user_interactions[user['title']]['comments'] += 1
                                elif 'Story Likes' in interaction['value']:
                                    user_interactions[user['title']]['story_likes'] += 1
                                elif 'Post Likes' in interaction['value']:
                                    user_interactions[user['title']]['post_likes'] += 1
            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")
    return user_interactions

def top_20_users(user_interactions):
    sorted_users = sorted(user_interactions.items(), key=lambda x: (x[1]['post_likes'] + x[1]['story_likes'] + x[1]['comments']), reverse=True)
    top_20_users = sorted_users[:20]
    return top_20_users

def write_to_csv(top_20_users):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, interactions in top_20_users:
            writer.writerow({'User': user, 'Post Likes': interactions['post_likes'], 'Story Likes': interactions['story_likes'], 'Comments': interactions['comments']})

def main():
    root_dir = "root_dir"
    try:
        user_interactions = get_user_interactions(root_dir)
        top_20_users_list = top_20_users(user_interactions)
        write_to_csv(top_20_users_list)
    except FileNotFoundError as e:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except Exception as e:
        raise ValueError("ValueError: " + str(e))

if __name__ == "__main__":
    main()