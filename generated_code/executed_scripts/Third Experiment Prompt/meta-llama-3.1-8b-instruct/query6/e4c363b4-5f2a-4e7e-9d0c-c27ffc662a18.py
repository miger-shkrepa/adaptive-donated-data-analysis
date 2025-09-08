import csv
import os
import json

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

    # Iterate over the directory structure
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == 'account_information.json':
                try:
                    with open(os.path.join(dirpath, filename), 'r') as file:
                        data = json.load(file)
                        for key, value in data.items():
                            if key == 'profile_account_insights':
                                for item in value:
                                    changed = item.get('string_map_data', {}).get('Name', {}).get('value', '')
                                    new_value = item.get('string_map_data', {}).get('Benutzername', {}).get('value', '')
                                    change_date = item.get('string_map_data', {}).get('Letzte Anmeldung', {}).get('value', '')
                                    writer.writerow({'Changed': changed, 'New Value': new_value, 'Change Date': change_date})
                            elif key == 'profile_note_interactions':
                                for item in value:
                                    changed = item.get('string_map_data', {}).get('Notizen zuletzt gesehen', {}).get('value', '')
                                    new_value = item.get('string_map_data', {}).get('Notizen zuletzt gesehen', {}).get('value', '')
                                    change_date = item.get('string_map_data', {}).get('Notizen zuletzt gesehen', {}).get('value', '')
                                    writer.writerow({'Changed': changed, 'New Value': new_value, 'Change Date': change_date})
                            elif key == 'profile_user':
                                for item in value:
                                    changed = item.get('string_map_data', {}).get('Name', {}).get('value', '')
                                    new_value = item.get('string_map_data', {}).get('Benutzername', {}).get('value', '')
                                    change_date = item.get('string_map_data', {}).get('Geburtsdatum', {}).get('value', '')
                                    writer.writerow({'Changed': changed, 'New Value': new_value, 'Change Date': change_date})
                            elif key == 'profile_business':
                                for item in value:
                                    changed = item.get('string_map_data', {}).get('Name', {}).get('value', '')
                                    new_value = item.get('string_map_data', {}).get('Name', {}).get('value', '')
                                    change_date = item.get('string_map_data', {}).get('Name', {}).get('value', '')
                                    writer.writerow({'Changed': changed, 'New Value': new_value, 'Change Date': change_date})
                            elif key == 'profile_profile_change':
                                for item in value:
                                    changed = item.get('string_map_data', {}).get('Change Date', {}).get('value', '')
                                    new_value = item.get('string_map_data', {}).get('New Value', {}).get('value', '')
                                    change_date = item.get('string_map_data', {}).get('Change Date', {}).get('value', '')
                                    writer.writerow({'Changed': changed, 'New Value': new_value, 'Change Date': change_date})
                except FileNotFoundError:
                    print(f"Error: File '{os.path.join(dirpath, filename)}' not found.")
                except json.JSONDecodeError as e:
                    print(f"Error: Failed to parse JSON in file '{os.path.join(dirpath, filename)}': {e}")
            elif filename == 'account_status_changes.json':
                try:
                    with open(os.path.join(dirpath, filename), 'r') as file:
                        data = json.load(file)
                        for key, value in data.items():
                            if key == 'account_history_account_active_status_changes':
                                for item in value:
                                    changed = item.get('string_map_data', {}).get('Art der Aktivierung', {}).get('value', '')
                                    new_value = item.get('string_map_data', {}).get('Grund fÃ¼r Deaktivierung', {}).get('value', '')
                                    change_date = item.get('string_map_data', {}).get('Zeit', {}).get('value', '')
                                    writer.writerow({'Changed': changed, 'New Value': new_value, 'Change Date': change_date})
                except FileNotFoundError:
                    print(f"Error: File '{os.path.join(dirpath, filename)}' not found.")
                except json.JSONDecodeError as e:
                    print(f"Error: Failed to parse JSON in file '{os.path.join(dirpath, filename)}': {e}")
            elif filename == 'account_privacy_changes.json':
                try:
                    with open(os.path.join(dirpath, filename), 'r') as file:
                        data = json.load(file)
                        for key, value in data.items():
                            if key == 'account_history_account_privacy_history':
                                for item in value:
                                    changed = item.get('string_map_data', {}).get('Zeit', {}).get('value', '')
                                    new_value = item.get('string_map_data', {}).get('Zeit', {}).get('value', '')
                                    change_date = item.get('string_map_data', {}).get('Zeit', {}).get('value', '')
                                    writer.writerow({'Changed': changed, 'New Value': new_value, 'Change Date': change_date})
                except FileNotFoundError:
                    print(f"Error: File '{os.path.join(dirpath, filename)}' not found.")
                except json.JSONDecodeError as e:
                    print(f"Error: Failed to parse JSON in file '{os.path.join(dirpath, filename)}': {e}")
            elif filename == 'last_known_location.json':
                try:
                    with open(os.path.join(dirpath, filename), 'r') as file:
                        data = json.load(file)
                        for key, value in data.items():
                            if key == 'account_history_imprecise_last_known_location':
                                for item in value:
                                    changed = item.get('string_map_data', {}).get('Ungenauer Breitengrad', {}).get('value', '')
                                    new_value = item.get('string_map_data', {}).get('Ungenauer LÃ¤ngengrad', {}).get('value', '')
                                    change_date = item.get('string_map_data', {}).get('Upload-Zeitpunkt', {}).get('value', '')
                                    writer.writerow({'Changed': changed, 'New Value': new_value, 'Change Date': change_date})
                except FileNotFoundError:
                    print(f"Error: File '{os.path.join(dirpath, filename)}' not found.")
                except json.JSONDecodeError as e:
                    print(f"Error: Failed to parse JSON in file '{os.path.join(dirpath, filename)}': {e}")
            elif filename == 'login_activity.json':
                try:
                    with open(os.path.join(dirpath, filename), 'r') as file:
                        data = json.load(file)
                        for key, value in data.items():
                            if key == 'account_history_login_history':
                                for item in value:
                                    changed = item.get('string_map_data', {}).get('IP-Adresse', {}).get('value', '')
                                    new_value = item.get('string_map_data', {}).get('User Agent', {}).get('value', '')
                                    change_date = item.get('string_map_data', {}).get('Zeit', {}).get('value', '')
                                    writer.writerow({'Changed': changed, 'New Value': new_value, 'Change Date': change_date})
                except FileNotFoundError:
                    print(f"Error: File '{os.path.join(dirpath, filename)}' not found.")
                except json.JSONDecodeError as e:
                    print(f"Error: Failed to parse JSON in file '{os.path.join(dirpath, filename)}': {e}")
            elif filename == 'logout_activity.json':
                try:
                    with open(os.path.join(dirpath, filename), 'r') as file:
                        data = json.load(file)
                        for key, value in data.items():
                            if key == 'account_history_logout_history':
                                for item in value:
                                    changed = item.get('string_map_data', {}).get('IP-Adresse', {}).get('value', '')
                                    new_value = item.get('string_map_data', {}).get('User Agent', {}).get('value', '')
                                    change_date = item.get('string_map_data', {}).get('Zeit', {}).get('value', '')
                                    writer.writerow({'Changed': changed, 'New Value': new_value, 'Change Date': change_date})
                except FileNotFoundError:
                    print(f"Error: File '{os.path.join(dirpath, filename)}' not found.")
                except json.JSONDecodeError as e:
                    print(f"Error: Failed to parse JSON in file '{os.path.join(dirpath, filename)}': {e}")
            elif filename == 'password_change_activity.json':
                try:
                    with open(os.path.join(dirpath, filename), 'r') as file:
                        data = json.load(file)
                        for key, value in data.items():
                            if key == 'account_history_password_change_history':
                                for item in value:
                                    changed = item.get('string_map_data', {}).get('Zeit', {}).get('value', '')
                                    new_value = item.get('string_map_data', {}).get('Zeit', {}).get('value', '')
                                    change_date = item.get('string_map_data', {}).get('Zeit', {}).get('value', '')
                                    writer.writerow({'Changed': changed, 'New Value': new_value, 'Change Date': change_date})
                except FileNotFoundError:
                    print(f"Error: File '{os.path.join(dirpath, filename)}' not found.")
                except json.JSONDecodeError as e:
                    print(f"Error: Failed to parse JSON in file '{os.path.join(dirpath, filename)}': {e}")
            elif filename == 'signup_information.json':
                try:
                    with open(os.path.join(dirpath, filename), 'r') as file:
                        data = json.load(file)
                        for key, value in data.items():
                            if key == 'account_history_registration_info':
                                for item in value:
                                    changed = item.get('string_map_data', {}).get('Benutzername', {}).get('value', '')
                                    new_value = item.get('string_map_data', {}).get('E-Mail-Adresse', {}).get('value', '')
                                    change_date = item.get('string_map_data', {}).get('Zeit', {}).get('value', '')
                                    writer.writerow({'Changed': changed, 'New Value': new_value, 'Change Date': change_date})
                except FileNotFoundError:
                    print(f"Error: File '{os.path.join(dirpath, filename)}' not found.")
                except json.JSONDecodeError as e:
                    print(f"Error: Failed to parse JSON in file '{os.path.join(dirpath, filename)}': {e}")