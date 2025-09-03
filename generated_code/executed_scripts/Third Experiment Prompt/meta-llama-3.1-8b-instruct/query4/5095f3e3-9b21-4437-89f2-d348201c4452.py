import csv
import json
import os

# Define the root directory
root_dir = "root_dir"

# Check if the root directory exists
if not os.path.exists(root_dir):
    raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")

# Initialize an empty list to store the company names
company_names = []

# Iterate over the directory structure
for filename in os.listdir(root_dir):
    if filename.endswith(".json"):
        with open(os.path.join(root_dir, filename), 'r') as json_file:
            data = json.load(json_file)
            if "your_instagram_activity" in data:
                for key, value in data["your_instagram_activity"].items():
                    if key == "avatars_store" or key == "events" or key == "fundraisers" or key == "gifts" or key == "instagram_live" or key == "meta_spark" or key == "monetization" or key == "other_activity" or key == "reports" or key == "shopping" or key == "story_interactions" or key == "subscriptions":
                        continue
                    if isinstance(value, dict):
                        for k, v in value.items():
                            if k == "structure":
                                for item in v:
                                    if "string_map_data" in item:
                                        for k2, v2 in item["string_map_data"].items():
                                            if k2 == "Name der Stadt" or k2 == "Benutzername" or k2 == "E-Mail-Adresse" or k2 == "Geburtsdatum" or k2 == "Geschlecht" or k2 == "Name" or k2 == "Privates Konto" or k2 == "Telefonnummer bestÃ¤tigt" or k2 == "Benutzername" or k2 == "E-Mail-Adresse" or k2 == "GerÃ¤t" or k2 == "IP-Adresse" or k2 == "Telefonnummer" or k2 == "Name des Produkts" or k2 == "Benutzername" or k2 == "Externe URL" or k2 == "Stummgeschaltete Creator":
                                                company_names.append(v2["value"])
                    elif isinstance(value, list):
                        for item in value:
                            if "string_map_data" in item:
                                for k2, v2 in item["string_map_data"].items():
                                    if k2 == "Name der Stadt" or k2 == "Benutzername" or k2 == "E-Mail-Adresse" or k2 == "Geburtsdatum" or k2 == "Geschlecht" or k2 == "Name" or k2 == "Privates Konto" or k2 == "Telefonnummer bestÃ¤tigt" or k2 == "Benutzername" or k2 == "E-Mail-Adresse" or k2 == "GerÃ¤t" or k2 == "IP-Adresse" or k2 == "Telefonnummer" or k2 == "Name des Produkts" or k2 == "Benutzername" or k2 == "Externe URL" or k2 == "Stummgeschaltete Creator":
                                        company_names.append(v2["value"])

# Write the company names to a CSV file
with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Company Name"])
    writer.writerows([[company_name] for company_name in company_names])