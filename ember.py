### EMBER 
### The focus of this file is to setup all the logs and folder structures 
### needed for the Ember to work
### Note : Ember won't be just one program but a multiple process combnations

import os
import sys
from read_input_file import pick_random_topic

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
