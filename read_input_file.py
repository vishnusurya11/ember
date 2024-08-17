import os
import random

def pick_random_topic(input_directory):
    """
    Picks a random file from the input directory and selects a random topic from that file.
    
    Parameters:
        input_directory (str): The directory containing input text files.
        
    Returns:
        dict: A dictionary with keys 'topic' and 'type', where 'topic' is a randomly selected topic from a randomly selected file, and 'type' is derived from the file name.
    """
    # List all text files in the directory
    files = [f for f in os.listdir(input_directory) if f.endswith('.txt')]
    
    if not files:
        raise FileNotFoundError("No text files found in the input directory.")
    
    # Pick a random file
    random_file = random.choice(files)
    file_path = os.path.join(input_directory, random_file)
    
    # Extract type from file name (remove extension)
    file_type = os.path.splitext(random_file)[0]
    
    # Read the file and pick a random topic
    with open(file_path, 'r') as file:
        topics = file.readlines()
    
    if not topics:
        raise ValueError(f"No topics found in the file: {random_file}")
    
    random_topic = random.choice(topics).strip()
    
    return {"topic": random_topic, "type": file_type}

if __name__ == "__main__":
    input_directory = r"D:\langchain\Ember\input"  # Replace with your actual input directory
    random_selection = pick_random_topic(input_directory)
    print(f"Randomly selected topic: {random_selection['topic']}, Type: {random_selection['type']}")
