"""
Second Prompt Based Experiment of Master Thesis.

:author: Miger Shkrepa
"""

from src import helper, evaluations
from pathlib import Path
import time
import uuid
import os
import llama_index_init
from llama_index.core.llms import ChatMessage

if __name__ == "__main__":
    # --- Configuration (user-defined) ---
    models = [
         "meta-llama-3.1-8b-instruct",
         "meta-llama-3.1-70b-instruct",
         "meta/llama-3.1-70b-instruct",
         "mistral-large-instruct",
         "codestral-22b",
         "qwen2.5-72b-instruct",
         "qwen2.5-coder-32b-instruct"
    ]
    queries = [
        "What topics does Instagram determine to be of interest for a user?",
        "How often does a user see advertisements and about which topics (from which companies)?",
        "How often do people see posts(daily and weekly)?",
        "Which companies have access to your Instagram activity or information?",
        "Which devices has the user logged in from and when?",
        "What Instagram account changes (e.g., name, phone, email) has the user made over time?",
        "Whose stories does the user tend to engage with most often?",
        "Which accounts has the user interacted with most often through post likes, story likes and comments(Top 20)?",
        "Which profiles does the user follow that do not follow him back?",
        "How often does the user view content (including both posts and videos) and from which accounts?",
        "Which accounts has the user viewed posts from but not liked them?",
        "How many messages does the user send per week?"
    ]
    query_CSV_instructions = [
        "The response must be a structured CSV file with one column: Topics of Interest.\n",
        "The response must be a structured CSV file with two columns: Company Name and Number of Ads Viewed.\n",
        "The response must be a structured CSV file with three columns: Date/Week, Posts Viewed and Type. The 'Type' column must contain either 'Daily' or 'Weekly' as values. The 'Date/Week' Column must follow the 'YYYY-MM-DD' format (e.g., 2025-01-18) for daily dates and the 'Week YYYY-WW' format (e.g., Week 2025-02) for weeks. The weekly value must be generated using strftime('%Y-%W'), where weeks start on Monday.\n",
        "The response must be a structured CSV file with one column: Company Name.\n",
        "The response must be a structured CSV file with two columns: Device ID and Login Time. The 'Login Time' column must follow the 'YYYY-MM-DD HH:MM:SS' format (e.g., 2025-01-21 12:46:26).\n",
        "The response must be a structured CSV file with three columns: Changed, New Value and Change Date. The 'Change Date' Column must follow the 'YYYY-MM-DD' format (e.g., 2025-01-18).\n",
        "The response must be a structured CSV file with two columns: User and Times Engaged.\n",
        "The response must be a structured CSV file with four columns: User, Post Likes, Story Likes and Comments.\n",
        "The response must be a structured CSV file with one column: Profile.\n",
        "The response must be a structured CSV file with three columns: Account,Post Views and Video Views.\n",
        "The response must be a structured CSV file with one column: Account.\n",
        "The response must be a structured CSV file with two columns: Week and Messages Sent. The 'Week' column must follow the 'Week YYYY-WW' format (e.g., Week 2025-02). The weekly value must be generated using strftime('%Y-%W'), where weeks start on Monday. Within the 'inbox' directory, each conversation is stored in its own subfolder. The folder names are anonymized or unique, so do not assume a fixed name like 'username_placeholder'. In each subfolder, look for one or more message_X.json files, where X is a sequential digit starting from 1 (e.g., message_1.json, message_2.json, ...). The files must be read in order, and there won't be gaps in numbering.\n"
    ]

    datasets_dir = Path("../datasets")
    ground_truths_base_dir = Path("../ground_truths")
    constants_path = "../constants.py"
    gen_script_path = "../generated_code/extracted_code.py"
    gen_result_path = "../query_responses/results.csv"


    # --- Helper to get dataset folder names ---
    def get_dataset_folders(directory: Path):
        return [folder for folder in directory.iterdir() if folder.is_dir()]


    # --- Helper to match dataset to ground truth ---
    def find_ground_truth(dataset_name: str, ground_truth_dir: Path):
        for gt_file in ground_truth_dir.glob("*.csv"):
            if dataset_name in gt_file.stem:
                return gt_file
        return None


    # --- Pipeline iteration ---
    dataset_folders = get_dataset_folders(datasets_dir)

    for query_idx, query in enumerate(queries):
        query_dir_name = f"query{query_idx + 1}"
        query_ground_truth_dir = ground_truths_base_dir / query_dir_name
        for model in models:
            selected_datasets = dataset_folders
            for dataset_folder in selected_datasets:
                if model == "meta-llama-3.1-8b-instruct":
                    dataset_name = dataset_folder.name
                    ground_truth_path = find_ground_truth(dataset_name, query_ground_truth_dir)

                    with open("../data/directory_structure_final.txt", "r", encoding="utf-8") as structure_file:
                        data_structure = structure_file.read()

                    settings = llama_index_init.init(llm_model_name=model)

                    # Now temporarily set local Settings
                    from llama_index.core import Settings

                    Settings.llm = settings["llm"]
                    Settings.embed_model = settings["embed_model"]

                    error_count = 0  # Track errors
                    error_message = None  # Stores the latest error
                    max_attempts = 5  # Allowed number of retries
                    experiment_id = str(uuid.uuid4())

                    # user_input = input("Enter your query: ")
                    user_input = ""
                    total_start_time = time.time()
                    base_prompt = (
                            "This is the tree structure of a directory containing user data: \n"
                            "'" + data_structure + "'\n"
                            "This directory consists of several nested folders, JSON files with unique structures, and other types of files. "
                            "I will ask you to generate Python scripts for unique queries based on this data. The generated code must follow the following rules:\n"
                            "1) The code must be designed such that the file input is the main folder, which corresponds to the main and first object in the structure.\n"
                            "2) The variable referring to the file input must be declared in a single line. For example: root_dir=\"value\"\n"
                            "3) The variable referring to the file input must have the value \"root_dir\".\n"
                            "4) Write the code using only standard Python libraries. Avoid external libraries such as pandas, numpy, etc.\n"
                            "5) The code must include proper error handling.\n"
                            "6) The code must raise proper Python exceptions (e.g., FileNotFoundError, ValueError). These exceptions must include the following: \"Error: \" and the reason for failure.\n"
                            "7) The errors must be structured in the format: raise FileNotFoundError(\"FileNotFoundError: The root directory does not exist.\")\n"
                            "8) " + query_CSV_instructions[query_idx] +
                            "9) Save the resulting CSV file at the path 'query_responses/results.csv'. This path refers solely to where the output file should be stored and should not be used or treated as part of the data directory being analyzed.\n"
                            "10) The code may be executed on incomplete or partially missing directories, so do not assume that all expected files will be present. If a required file for answering the question does not exist, return a CSV file containing only the column headers. If the missing file contributes to only part of the aggregation or calculation(e.g., one of multiple columns), treat its contribution as 0 and continue processing the rest.\n"
                    )

                    error_instructions = ""
                    while error_count <= max_attempts:
                        full_prompt = (base_prompt +
                                       "Based on the directory structure, I would like you to create a Python script that answers the following query: " +
                                       query +
                                       user_input +
                                       error_instructions)
                        messages = [
                            ChatMessage(role="system", content="You are a helpful assistant."),
                            ChatMessage(role="user", content=full_prompt)
                        ]

                        # Use chat interface
                        response = Settings.llm.chat(messages)

                        helper.extract_code(str(response), gen_script_path)
                        helper.modify_root_dir(gen_script_path, f"datasets/{dataset_name}")
                        result = helper.run_python_script(experiment_id,
                                                          model,
                                                          error_count + 1,
                                                          gen_script_path)

                        if not result["error"]:
                            total_end_time = time.time()
                            total_duration = round(total_end_time - total_start_time, 2)
                            print(f"\n✅ Script ran successfully. Total execution time: {total_duration} seconds.")

                            # Save the script for tracking
                            with open(gen_script_path, "r", encoding="utf-8") as script_file:
                                latest_generated_code = script_file.read()

                            latest_generated_code = helper.demodify_root_dir(latest_generated_code)

                            os.makedirs(f"generated_code/executed_scripts/Second Experiment Prompt/{model}/{query_dir_name}", exist_ok=True)
                            with open(f"generated_code/executed_scripts/Second Experiment Prompt/{model}/{query_dir_name}/{experiment_id}.py", "w",
                                      encoding="utf-8") as f:
                                f.write(latest_generated_code)

                            evaluations.evaluate_accuracy_and_log(experiment_id,
                                                                  dataset_name,
                                                                  model,
                                                                  query,
                                                                  ground_truth_path,
                                                                  gen_result_path,
                                                                  error_count,
                                                                  result["code_exec_time"],
                                                                  total_duration)
                            evaluations.evaluate_generated_code_and_log(experiment_id,
                                                                        model,
                                                                        query,
                                                                        gen_script_path)
                            break

                        if result["error"]:
                            if error_count > 0:
                                print(f"\n❌ Error detected: {result["error"]} (Retry {error_count}/{max_attempts})")
                            else:
                                print(f"\n❌ Error detected: {result["error"]}")

                            error_count += 1
                            error_message = result["error"]

                            with open(gen_script_path, "r", encoding="utf-8") as script_file:
                                latest_generated_code = script_file.read()

                            latest_generated_code = helper.demodify_root_dir(latest_generated_code)

                            error_instructions = ""
                            # Append both the error message and the previously generated script to the prompt
                            error_instructions += (
                                f'\n\nThe last code you generated was:\n```python\n{latest_generated_code}\n```\n'
                                f'Avoid the following error that occurred for this script: "{error_message}".'
                            )

                    with open(gen_script_path, 'w') as file:
                        pass

                    if error_count > max_attempts:
                        total_end_time = time.time()  # Total end time if max retries reached
                        total_duration = round(total_end_time - total_start_time, 2)  # Total duration
                        print(f"\n❌ The model wasn't able to produce any results for your query. Stopping execution. "
                              f"Total execution time: {total_duration} seconds.")
                        evaluations.log_unsuccesful_trial(experiment_id,
                                                          dataset_name,
                                                          model,
                                                          query,
                                                          error_count,
                                                          total_duration)
