import csv
import os

root_dir = "root_dir"

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON.")

def extract_ad_data(json_data):
    ad_data = []
    for post in json_data['likes']['liked_posts.json']['structure']['likes_media_likes']:
        ad_data.append({
            'company_name': post['title'],
            'number_of_ads_viewed': len(post['string_list_data'])
        })
    return ad_data

def process_data(root_dir):
    ad_data = []
    for file in os.listdir(root_dir):
        file_path = os.path.join(root_dir, file)
        if os.path.isfile(file_path):
            if file.endswith('.json'):
                json_data = load_json_file(file_path)
                ad_data.extend(extract_ad_data(json_data))
    return ad_data

def save_to_csv(data, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['Company Name', 'Number of Ads Viewed'])
        writer.writeheader()
        writer.writerows(data)

try:
    ad_data = process_data(root_dir)
    save_to_csv(ad_data, 'query_responses/results.csv')
except Exception as e:
    raise Exception("Error: " + str(e))