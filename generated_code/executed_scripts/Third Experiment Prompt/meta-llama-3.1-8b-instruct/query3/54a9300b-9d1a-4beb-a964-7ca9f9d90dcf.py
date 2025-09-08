import os
import csv
import datetime
import json

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Date/Week', 'Posts Viewed', 'Type'])

    # Iterate over the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.json'):
                filepath = os.path.join(dirpath, filename)
                try:
                    with open(filepath, 'r') as json_file:
                        data = json.load(json_file)
                        if 'ads_information' in data and 'ads_and_topics' in data['ads_information'] and 'ads_viewed.json' in data['ads_and_topics']:
                            # Extract the impressions history ads seen data
                            impressions_history_ads_seen = data['ads_information']['ads_and_topics']['ads_viewed.json']['structure']['impressions_history_ads_seen']
                            for impression in impressions_history_ads_seen:
                                string_map_data = impression['string_map_data']
                                author = string_map_data.get('Author', {}).get('value')
                                time = string_map_data.get('Time', {}).get('timestamp')
                                if author and time:
                                    # Determine the date or week
                                    date = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d')
                                    week = datetime.datetime.fromtimestamp(time).strftime('%Y-%W')
                                    # Write the data to the CSV file
                                    writer.writerow([date, 1, 'Daily'])
                                    writer.writerow([week, 1, 'Weekly'])
                        elif 'logged_information' in data and 'recent_searches' in data['logged_information'] and 'profile_searches.json' in data['logged_information']['recent_searches']:
                            # Extract the searches user data
                            searches_user = data['logged_information']['recent_searches']['profile_searches.json']['structure']['searches_user']
                            for search in searches_user:
                                string_map_data = search['string_map_data']
                                search_time = string_map_data.get('Time', {}).get('timestamp')
                                if search_time:
                                    # Determine the date or week
                                    date = datetime.datetime.fromtimestamp(search_time).strftime('%Y-%m-%d')
                                    week = datetime.datetime.fromtimestamp(search_time).strftime('%Y-%W')
                                    # Write the data to the CSV file
                                    writer.writerow([date, 1, 'Daily'])
                                    writer.writerow([week, 1, 'Weekly'])
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON file: {e}")
                except KeyError as e:
                    print(f"Error accessing key: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")