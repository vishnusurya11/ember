# main.py

from story_prompt import generate_short_script, improve_story  
import json
from datetime import datetime

def main():
    # Define the topic for the story generation
    input_dict = {'topic': 'a space story based on any detective story'}
    
    # Generate the initial story
    print("Generating the initial story...")
    story = generate_short_script(input_dict)
    
    # Specify the number of improvement iterations
    iterations = 2
    
    # Improve the generated story
    print("\nImproving the story...")
    improved_story = improve_story(story, iterations=iterations)
    print(improved_story)
    # Create a dictionary to include the story
    story_dict = {
        "story": improved_story
    }
    
    # Generate the filename based on the current time
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"data/script_{timestamp}.json"
    
    # Save the dictionary to a JSON file
    with open(filename, 'w') as f:
        json.dump(story_dict, f, indent=4)
    
    # Print the location of the saved file
    print(f"\nStory saved to {filename}")

if __name__ == "__main__":
    main()
