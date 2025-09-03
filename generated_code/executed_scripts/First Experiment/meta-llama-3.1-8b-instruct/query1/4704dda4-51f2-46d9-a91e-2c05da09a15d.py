import csv
import os

def get_topics_of_interest(root_dir):
    try:
        topics_of_interest = []
        for filename in os.listdir(root_dir):
            if filename.endswith(".json"):
                with open(os.path.join(root_dir, filename), 'r') as file:
                    data = file.read()
                    if "instagram_profile_information.json" in data:
                        json_data = eval(data)
                        for profile_account_insights in json_data["profile_account_insights"]:
                            for string_map_data in profile_account_insights["string_map_data"].values():
                                if "label" in string_map_data:
                                    topics_of_interest.append(string_map_data["label"])
        return topics_of_interest
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
    except Exception as e:
        raise ValueError("ValueError: An error occurred while processing the data.")

root_dir = "root_dir"
topics_of_interest = get_topics_of_interest(root_dir)

with open('query_responses/results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Topics of Interest"])
    for topic in topics_of_interest:
        writer.writerow([topic])