import yaml
import os


def load_config(config_path: str):
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    # Create and return the StoryConfig object
    return config


def get_base_data_folder():
    # Get the current working directory (CWD)
    cwd = os.getcwd()

    # If 'PROD' is in the current working directory, use the production base folder
    if "PROD" in cwd:
        base_data_folder = r"E:\PRODUCTION\Ember\ember\data"
        plot_file = r"E:\PRODUCTION\Ember\ember\flash-fiction-plots-yaml.yaml"
        input_mp3_path = r"E:\PRODUCTION\Ember\ember\sample_5.mp3"
    else:
        # Use the alternate base data folder
        base_data_folder = r"E:\Ember\Ember\ember\data"
        plot_file = r"E:\Ember\Ember\ember\flash-fiction-plots-yaml.yaml"
        input_mp3_path = r"sample_5.mp3"

    return base_data_folder, plot_file, input_mp3_path
