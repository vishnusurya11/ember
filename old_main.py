# EMBER
# The focus of this file is to setup all the logs and folder structures
# needed for the Ember to work
# Note : Ember won't be just one program but a multiple process combnations
"""
TODO:
Currently, the topic is chosen randomly from a file. The goal is to modify the system so that topics are selected from a DataFrame instead.
In this setup, each row will represent a record, and each column will represent a specific topic, such as 'fun fact,' 'location,' or any other
interesting details that can be used as a short script. New rows and columns will be added over time. Once a topic is selected, it should be
marked (e.g., with an 'x' or another indicator), so that in subsequent rounds, only the unmarked topics will be eligible for selection.
This approach will maintain randomness while ensuring that each topic is eventually used.
"""

import os
import sys
from read_input_file import pick_random_topic
from chat_model import generate_short_script


def create_folders_if_not_exist(base_directory, folders):
    for folder in folders:
        folder_path = os.path.join(base_directory, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created folder: {folder_path}")
        else:
            print(f"Folder already exists: {folder_path}")


if __name__ == "__main__":
    base_directory = r"D:\langchain\Ember"
    input_files_directory = r"D:\langchain\Ember\input"
    folders_to_create = ["input", "logs"]  # Replace with your folder names
    create_folders_if_not_exist(base_directory, folders_to_create)

    # Pick a random topic from the input directory
    random_topic = pick_random_topic(input_files_directory)
    print(f"Randomly selected topic: {random_topic}")

    result = generate_short_script(random_topic)
    print(result)
