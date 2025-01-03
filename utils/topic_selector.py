# import yaml
# import random


# def plot_selector(yaml_file):
#     # Read the YAML file
#     with open(yaml_file, "r", encoding="utf-8") as file:
#         data = yaml.safe_load(file)


#     # Check if there are any plots in unused_plots
#     if not data["unused_plots"]:
#         return "No plots left in unused_plots."

#     # Randomly select a key from unused_plots
#     selected_key = random.choice(list(data["unused_plots"].keys()))
#     selected_plot = data["unused_plots"].pop(selected_key)

#     # Move the selected plot to used_plots
#     data["used_plots"].append({selected_key: selected_plot})

#     # Write the updated data back to the YAML file
#     with open(yaml_file, "w") as file:
#         yaml.dump(data, file, default_flow_style=False)

#     # Return the selected plot
#     return selected_plot


import random
import yaml


def plot_selector(yaml_file):
    # Read the YAML file
    with open(yaml_file, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    # Check if there are any plots in unused_plots
    if not data["unused_plots"]:
        return "No plots left in unused_plots."

    # Randomly select a plot from unused_plots (since it's a list, no keys)
    selected_plot = random.choice(data["unused_plots"])

    # Remove the selected plot from unused_plots
    data["unused_plots"].remove(selected_plot)

    # Move the selected plot to used_plots
    data["used_plots"].append(selected_plot)

    # Write the updated data back to the YAML file
    with open(yaml_file, "w", encoding="utf-8") as file:
        yaml.dump(data, file, default_flow_style=False)

    # Return the selected plot
    return selected_plot


if __name__ == "__main__":
    yaml_file = "plots.yaml"  # Path to your YAML file
    selected_plot = pick_and_move_plot(yaml_file)
    print(selected_plot)
