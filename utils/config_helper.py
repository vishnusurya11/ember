import yaml


def load_config(config_path: str):
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    # Create and return the StoryConfig object
    return config
