import csv
import os

root_dir = "root_dir"

def get_post_likes():
    post_likes = {}
    try:
        for filename in os.listdir(root_dir):
            if filename.endswith(".json"):
                with open(os.path.join(root_dir, filename), 'r') as file:
                    data = eval(file.read())
                    if 'story_activities_story_likes' in data['structure']:
                        for item in data['structure']['story_activities_story_likes']:
                            if 'string_list_data' in item:
                                for item2 in item['string_list_data']:
                                    if 'timestamp' in item2:
                                        post_likes[item['title']] = post_likes.get(item['title'], 0) + 1
                    if 'story_activities_quizzes' in data['structure']:
                        for item in data['structure']['story_activities_quizzes']:
                            if 'string_list_data' in item:
                                for item2 in item['string_list_data']:
                                    if 'timestamp' in item2:
                                        post_likes[item['title']] = post_likes.get(item['title'], 0) + 1
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    return post_likes

def get_story_likes():
    story_likes = {}
    try:
        for filename in os.listdir(root_dir):
            if filename.endswith(".json"):
                with open(os.path.join(root_dir, filename), 'r') as file:
                    data = eval(file.read())
                    if 'story_activities_story_likes' in data['structure']:
                        for item in data['structure']['story_activities_story_likes']:
                            if 'string_list_data' in item:
                                for item2 in item['string_list_data']:
                                    if 'timestamp' in item2:
                                        story_likes[item['title']] = story_likes.get(item['title'], 0) + 1
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    return story_likes

def get_comments():
    comments = {}
    try:
        for filename in os.listdir(root_dir):
            if filename.endswith(".json"):
                with open(os.path.join(root_dir, filename), 'r') as file:
                    data = eval(file.read())
                    if 'story_activities_story_likes' in data['structure']:
                        for item in data['structure']['story_activities_story_likes']:
                            if 'string_list_data' in item:
                                for item2 in item['string_list_data']:
                                    if 'timestamp' in item2:
                                        comments[item['title']] = comments.get(item['title'], 0) + 1
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    return comments

def get_top_interacted_accounts():
    post_likes = get_post_likes()
    story_likes = get_story_likes()
    comments = get_comments()
    top_interacted_accounts = {}
    for account in post_likes:
        top_interacted_accounts[account] = post_likes[account] + story_likes.get(account, 0) + comments.get(account, 0)
    top_interacted_accounts = dict(sorted(top_interacted_accounts.items(), key=lambda item: item[1], reverse=True))
    return dict(list(top_interacted_accounts.items())[:20])

def write_to_csv(data):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        fieldnames = ['User', 'Post Likes', 'Story Likes', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for account, value in data.items():
            writer.writerow({'User': account, 'Post Likes': post_likes.get(account, 0), 'Story Likes': story_likes.get(account, 0), 'Comments': comments.get(account, 0)})

try:
    post_likes = get_post_likes()
    story_likes = get_story_likes()
    comments = get_comments()
    top_interacted_accounts = get_top_interacted_accounts()
    write_to_csv(top_interacted_accounts)
except Exception as e:
    raise Exception("Error: " + str(e))