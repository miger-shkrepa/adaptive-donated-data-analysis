import os
import csv
import json

root_dir = "root_dir"

def get_account_views(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            views = {}
            if 'recently_viewed_items.json' in data:
                for item in data['recently_viewed_items.json']['structure']['checkout_saved_recently_viewed_products']:
                    merchant_name = item['string_map_data']['Merchant Name']['value']
                    if merchant_name not in views:
                        views[merchant_name] = {'Post Views': 0, 'Video Views': 0}
                    # Assuming all viewed items are posts, as video views are not specified in the structure
                    views[merchant_name]['Post Views'] += 1
            return views
    except FileNotFoundError:
        raise FileNotFoundError("FileNotFoundError: The file does not exist.")
    except json.JSONDecodeError:
        raise ValueError("ValueError: The file is not a valid JSON.")
    except Exception as e:
        raise Exception(f"Error: An unexpected error occurred - {str(e)}")

def main():
    try:
        if not os.path.exists(root_dir):
            raise FileNotFoundError("FileNotFoundError: The root directory does not exist.")
        
        shopping_dir = os.path.join(root_dir, 'shopping')
        if not os.path.exists(shopping_dir):
            with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Account', 'Post Views', 'Video Views'])
            return
        
        views = {}
        for filename in os.listdir(shopping_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(shopping_dir, filename)
                account_views = get_account_views(file_path)
                for account, view_counts in account_views.items():
                    if account not in views:
                        views[account] = {'Post Views': 0, 'Video Views': 0}
                    views[account]['Post Views'] += view_counts['Post Views']
                    views[account]['Video Views'] += view_counts['Video Views']
        
        with open('query_responses/results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Account', 'Post Views', 'Video Views'])
            for account, view_counts in views.items():
                writer.writerow([account, view_counts['Post Views'], view_counts['Video Views']])
    
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()