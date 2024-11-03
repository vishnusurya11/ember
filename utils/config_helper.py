import yaml
import os
import random

def load_config(config_path: str):
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    # Create and return the StoryConfig object
    return config


def get_base_data_folder():
    # Get the current working directory (CWD)
    cwd = os.getcwd()

    # Define the range for random selection of mp3 files
    sample_file = f"sample_{random.randint(1, 7)}.mp3"

    # If 'PROD' is in the current working directory, use the production base folder
    if "PROD" in cwd:
        base_data_folder = r"E:\PRODUCTION\Ember\ember\data"
        plot_file = r"E:\PRODUCTION\Ember\ember\flash-fiction-plots-yaml.yaml"
        input_mp3_path = os.path.join(r"E:\PRODUCTION\Ember\ember", sample_file)
    else:
        # Use the alternate base data folder
        base_data_folder = r"E:\Ember\Ember\ember\data"
        plot_file = r"E:\Ember\Ember\ember\flash-fiction-plots-yaml.yaml"
        input_mp3_path = sample_file  # Only the filename if in the local setup

    return base_data_folder, plot_file, input_mp3_path
