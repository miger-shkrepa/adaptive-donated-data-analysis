import csv
import os

root_dir = "root_dir"

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON.")

def get_advertisements(root_dir):
    advertisements = {}
    for file in os.listdir(root_dir):
        file_path = os.path.join(root_dir, file)
        if file.endswith('.json'):
            data = load_json(file_path)
            for item in data['story_activities_quizzes']:
                if 'string_list_data' in item:
                    for ad in item['string_list_data']:
                        if 'value' in ad:
                            company = ad['value'].split('-')[0]
                            if company not in advertisements:
                                advertisements[company] = 0
                            advertisements[company] += 1
    return advertisements

def save_to_csv(advertisements):
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Company Name', 'Number of Ads Viewed'])
        for company, count in advertisements.items():
            writer.writerow([company, count])

try:
    advertisements = get_advertisements(root_dir)
    save_to_csv(advertisements)
except Exception as e:
    print(f"Error: {e}")
    with open('query_responses/results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Company Name', 'Number of Ads Viewed'])