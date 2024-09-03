from story_prompt import generate_short_script, improve_story, split_story_into_sentences  
from audio_gen import generate_audio_from_json
from prompt_generator import generate_prompts_for_sentences
from image_generator import generate_images_for_prompts, extract_timestamp_from_path  # Assuming you save the previous script as image_generator.py
import json
from datetime import datetime
import os

if __name__ == "__main__":
    # Define the data folder path provided as input
    base_data_folder = 'E:\\Ember\\Ember\\ember\\data'
    
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
    
    # Create the final dictionary to save
    story_dict = {
        "story": improved_story,
        "sentences": split_story_into_sentences(improved_story)
    }
    
    # Generate the filename and folder based on the current time
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    folder_name = os.path.join(base_data_folder, timestamp)
    os.makedirs(folder_name, exist_ok=True)
    
    filename = os.path.join(folder_name, f"script_{timestamp}.json")
    
    # Save the dictionary to a JSON file
    with open(filename, 'w') as f:
        json.dump(story_dict, f, indent=4)
    
    # Print the location of the saved file
    print(f"\nStory saved to {filename}")
    
    # Generate prompts for the sentences
    print("\nGenerating prompts for each sentence...")
    sentences_with_prompts = generate_prompts_for_sentences(story_dict.get("sentences", {}))
    story_dict["sentences"] = sentences_with_prompts

    # Save the updated JSON file with prompts
    with open(filename, 'w') as f:
        json.dump(story_dict, f, indent=4)
    
    print(f"Updated JSON with prompts saved to {filename}")
    
    # Call the audio generation function using the folder path
    input_mp3_path = 'sample_4.mp3'  # You can update this path if needed
    wav_path, mp3_path = generate_audio_from_json(folder_name, input_mp3=input_mp3_path)
    
    # Update the JSON file with the audio output path
    story_dict["audio_output"] = mp3_path
    with open(filename, 'w') as f:
        json.dump(story_dict, f, indent=4)
    
    print(f"Generated audio files:\nWAV: {wav_path}\nMP3: {mp3_path}")
    
    # Server and workflow configurations for image generation
    SERVER_ADDRESS = "127.0.0.1:8188"
    WORKFLOW_FILE = "flux_dev_space_example_16.json"
    SAVE_DIR = folder_name

    # Generate images for the prompts
    print("\nGenerating images for the prompts...")
    generate_images_for_prompts(SERVER_ADDRESS, WORKFLOW_FILE, SAVE_DIR, story_dict.get("sentences", {}), timestamp)

    # Define the final image output path
    final_image_folder = f"E:\\ComfyUI_windows_portable\\ComfyUI\\output\\api\\{timestamp}"
    story_dict["images_output"] = final_image_folder

    # Save the final JSON file with all outputs (prompts, audio, images)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(story_dict, f, indent=4)
    
    print(f"Final JSON with all outputs saved to {filename}")
