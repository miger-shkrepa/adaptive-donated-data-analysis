import os
import json
import csv

root_dir = "root_dir"

def get_number_of_ads_viewed(root_dir):
    try:
        ads_viewed_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "ads_viewed.json")
        if not os.path.exists(ads_viewed_path):
            raise FileNotFoundError("FileNotFoundError: The ads_viewed.json file does not exist.")
        
        with open(ads_viewed_path, 'r') as file:
            ads_viewed_data = json.load(file)
            number_of_ads_viewed = len(ads_viewed_data["impressions_history_ads_seen"])
            return number_of_ads_viewed
    
    except FileNotFoundError as e:
        raise FileNotFoundError("Error: " + str(e))

def get_company_names_and_topics(root_dir):
    try:
        accounts_youre_not_interested_in_path = os.path.join(root_dir, "ads_information", "ads_and_topics", "accounts_you're_not_interested_in.json")
        if not os.path.exists(accounts_youre_not_interested_in_path):
            raise FileNotFoundError("FileNotFoundError: The accounts_you're_not_interested_in.json file does not exist.")
        
        with open(accounts_youre_not_interested_in_path, 'r') as file:
            accounts_youre_not_interested_in_data = json.load(file)
            company_names_and_topics = {}
            for item in accounts_youre_not_interested_in_data["impressions_history_recs_hidden_authors"]:
                company_name = item["string_map_data"]["Benutzername"]["value"]
                topic = item["title"]
                if company_name not in company_names_and_topics:
                    company_names_and_topics[company_name] = [topic]
                else:
                    company_names_and_topics[company_name].append(topic)
            return company_names_and_topics
    
    except FileNotFoundError as e:
        raise FileNotFoundError("Error: " + str(e))

def write_to_csv(root_dir):
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        company_names_and_topics = get_company_names_and_topics(root_dir)
        number_of_ads_viewed = get_number_of_ads_viewed(root_dir)
        
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company_name, topics in company_names_and_topics.items():
                writer.writerow([company_name, number_of_ads_viewed])
    
    except FileNotFoundError as e:
        raise FileNotFoundError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

try:
    write_to_csv(root_dir)
except FileNotFoundError as e:
    with open('query_responses/results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
    print("Error: " + str(e))
except Exception as e:
    with open('query_responses/results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Company Name", "Number of Ads Viewed"])
    print("Error: " + str(e))