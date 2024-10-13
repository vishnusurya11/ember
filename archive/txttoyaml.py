import yaml


# Define a function to parse the text file and convert it to the YAML format
def parse_and_convert_to_yaml(input_file, output_file):
    with open(input_file, "r") as file:
        lines = file.readlines()

    # Create a dictionary for the unused plots
    unused_plots = {}
    counter = 1

    # Loop through the lines and store them in the dictionary
    for line in lines:
        line = line.strip()  # Remove any extra spaces or newlines
        if line:  # Check if the line is not empty
            unused_plots[counter] = line
            counter += 1

    # Structure the YAML data
    yaml_data = {"unused_plots": unused_plots, "used_plots": []}

    # Convert the dictionary to YAML and save it to the output file
    with open(output_file, "w") as yaml_file:
        yaml.dump(yaml_data, yaml_file, default_flow_style=False)


# Example usage
input_file = "input_plots.txt"  # Path to your input text file
output_file = "plots.yaml"  # Path to save the output YAML file

# Call the function to parse and convert the data
parse_and_convert_to_yaml(input_file, output_file)

print(f"YAML file has been saved to {output_file}")
