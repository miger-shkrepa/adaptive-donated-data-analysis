import csv
import os
import datetime

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize the CSV writer
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    fieldnames = ['Changed', 'New Value', 'Change Date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()

    # Iterate over the JSON files in the directory
    for filename in os.listdir(root_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(root_dir, filename)
            with open(filepath, 'r') as json_file:
                data = json.load(json_file)

                # Check if the JSON file contains the necessary data
                if 'monetization' in data and 'eligibility.json' in data['monetization']:
                    eligibility_data = data['monetization']['eligibility.json']['structure']['monetization_eligibility']

                    # Iterate over the monetization eligibility data
                    for item in eligibility_data:
                        # Check if the item contains the necessary data
                        if 'string_map_data' in item and 'Name des Produkts' in item['string_map_data']:
                            name = item['string_map_data']['Name des Produkts']['value']
                            timestamp = item['string_map_data']['Name des Produkts']['timestamp']

                            # Convert the timestamp to a date string
                            date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

                            # Write the data to the CSV file
                            writer.writerow({'Changed': 'Name', 'New Value': name, 'Change Date': date})

                # Check if the JSON file contains the necessary data
                if 'secret_conversations.json' in data:
                    secret_conversations_data = data['secret_conversations.json']['structure']['ig_secret_conversations']

                    # Iterate over the secret conversations data
                    for device in secret_conversations_data['armadillo_devices']:
                        # Check if the device contains the necessary data
                        if 'device_manufacturer' in device and 'device_model' in device:
                            manufacturer = device['device_manufacturer']
                            model = device['device_model']

                            # Write the data to the CSV file
                            writer.writerow({'Changed': 'Device Manufacturer', 'New Value': manufacturer, 'Change Date': date})

                # Check if the JSON file contains the necessary data
                if 'recently_unfollowed_accounts.json' in data:
                    recently_unfollowed_accounts_data = data['recently_unfollowed_accounts.json']['structure']['relationships_unfollowed_users']

                    # Iterate over the recently unfollowed accounts data
                    for item in recently_unfollowed_accounts_data:
                        # Check if the item contains the necessary data
                        if 'string_list_data' in item and 'value' in item['string_list_data'][0]:
                            value = item['string_list_data'][0]['value']

                            # Write the data to the CSV file
                            writer.writerow({'Changed': 'Unfollowed Account', 'New Value': value, 'Change Date': date})

                # Check if the JSON file contains the necessary data
                if 'restricted_accounts.json' in data:
                    restricted_accounts_data = data['restricted_accounts.json']['structure']['relationships_restricted_users']

                    # Iterate over the restricted accounts data
                    for item in restricted_accounts_data:
                        # Check if the item contains the necessary data
                        if 'string_list_data' in item and 'value' in item['string_list_data'][0]:
                            value = item['string_list_data'][0]['value']

                            # Write the data to the CSV file
                            writer.writerow({'Changed': 'Restricted Account', 'New Value': value, 'Change Date': date})

                # Check if the JSON file contains the necessary data
                if 'recent_follow_requests.json' in data:
                    recent_follow_requests_data = data['recent_follow_requests.json']['structure']['relationships_permanent_follow_requests']

                    # Iterate over the recent follow requests data
                    for item in recent_follow_requests_data:
                        # Check if the item contains the necessary data
                        if 'string_list_data' in item and 'value' in item['string_list_data'][0]:
                            value = item['string_list_data'][0]['value']

                            # Write the data to the CSV file
                            writer.writerow({'Changed': 'Follow Request', 'New Value': value, 'Change Date': date})

                # Check if the JSON file contains the necessary data
                if 'story_interactions.json' in data:
                    story_interactions_data = data['story_interactions.json']['structure']['story_activities_story_likes']

                    # Iterate over the story interactions data
                    for item in story_interactions_data:
                        # Check if the item contains the necessary data
                        if 'string_list_data' in item and 'timestamp' in item['string_list_data'][0]:
                            timestamp = item['string_list_data'][0]['timestamp']

                            # Convert the timestamp to a date string
                            date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

                            # Write the data to the CSV file
                            writer.writerow({'Changed': 'Story Like', 'New Value': '', 'Change Date': date})