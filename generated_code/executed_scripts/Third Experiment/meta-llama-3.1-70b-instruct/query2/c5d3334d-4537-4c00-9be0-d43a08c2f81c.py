import os
import json
import csv

root_dir = "root_dir"

def get_company_ads(root_dir):
    company_ads = {}
    try:
        ads_dir = os.path.join(root_dir, "ads_information", "instagram_ads_and_businesses")
        if not os.path.exists(ads_dir):
            raise FileNotFoundError("FileNotFoundError: The ads directory does not exist.")
        
        for filename in os.listdir(ads_dir):
            if filename == "ads_about_meta.json":
                file_path = os.path.join(ads_dir, filename)
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    for label_value in data["label_values"]:
                        if "label" in label_value:
                            company = label_value["label"]
                            if company not in company_ads:
                                company_ads[company] = 1
                            else:
                                company_ads[company] += 1
    except FileNotFoundError as e:
        raise FileNotFoundError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))
    return company_ads

def write_to_csv(company_ads):
    try:
        with open('query_responses/results.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Company Name", "Number of Ads Viewed"])
            for company, ads in company_ads.items():
                writer.writerow([company, ads])
    except Exception as e:
        raise ValueError("Error: " + str(e))

def main():
    try:
        company_ads = get_company_ads(root_dir)
        if not company_ads:
            with open('query_responses/results.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Company Name", "Number of Ads Viewed"])
        else:
            write_to_csv(company_ads)
    except FileNotFoundError as e:
        raise FileNotFoundError("Error: " + str(e))
    except Exception as e:
        raise ValueError("Error: " + str(e))

if __name__ == "__main__":
    main()