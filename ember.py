import json
from datetime import datetime
import os
import time
from dotenv import load_dotenv
from utils.config_helper import load_config, get_base_data_folder
from utils.topic_selector import plot_selector
import yaml
import random
from story_generator import (
    generate_short_script,
    improve_story,
    generate_youtube_title_description,
    generate_story,
)
from prompt_generator import generate_prompts_for_sentences, split_story_into_sentences, generate_thumbnail_prompt
from audio_generator import generate_audio_from_json
from image_generator import generate_images_for_prompts, extract_timestamp_from_path, generate_thumbnail
from video_generator import generate_and_concatenate_videos
from langchain_openai import ChatOpenAI

"""
TODO :
- Fix the prompts to be specific to the audio
- change the image format
- add a constants file
"""

if __name__ == "__main__":
    ##########################################################################
    ############################### 0 - Initial setup ########################
    ##########################################################################
    # Start measuring the time
    start_time = time.time()
    model = ChatOpenAI(model="gpt-4o-mini")
    # load_dotenv()
    # Define the data folder path provided as input
    # base_data_folder = r"E:\PRODUCTION\Ember\ember\data"
    # plot_file = r"E:\PRODUCTION\Ember\ember\flash-fiction-plots-yaml.yaml"
    # TODO : base folder setup function to be added to all files 
    # base_data_folder = "E:\\Ember\\Ember\\ember\\data"
    # # # plot_file = r"E:\Ember\Ember\ember\plots.yaml"
    # plot_file = r"E:\Ember\Ember\ember\flash-fiction-plots-yaml.yaml"
    base_data_folder, plot_file, input_mp3_path = get_base_data_folder()
    # TODO : base folder setup function to be added to all files
    # Generate the filename and folder based on the current time
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    folder_name = os.path.join(base_data_folder, timestamp)
    os.makedirs(folder_name, exist_ok=True)

    filename = os.path.join(folder_name, f"codex_{timestamp}.json")

    # Define the topic for the story generation
    # TODO - make the topic picking dynamic
    input_dict = {"topic": plot_selector(plot_file)}
    # TODO - Update the input audio files folder and create a library to
    # choose from
    # input_mp3_path = r"E:\PRODUCTION\Ember\ember\sample_5.mp3" #TODO - make it dynamic
    # input_mp3_path = r"sample_5.mp3" #TODO - make it dynamic
    ##########################################################################
    ############################### 1 - Story Generator ######################
    ##########################################################################
    # Generate the initial story
    print("Generating the initial story...")
    # story = generate_short_script(input_dict)
    story = generate_story(model, input_dict)
    print(f"input_dict --> {input_dict}")
    print(f"###############################################################")
    print(f"story --> {story}")
    print(f"###############################################################")
    # Specify the number of improvement iterations
    iterations = 3

    # Improve the generated story
    print("\nImproving the story...")
    # improved_story = improve_story(story, iterations=iterations)
    improved_story = story
    print(improved_story)
    youtube_details = generate_youtube_title_description(improved_story)
    # Create the final dictionary to save
    story_dict = {
        "story": improved_story,
        "youtube_details": youtube_details,
    }

    # Save the dictionary to a JSON file
    with open(filename, "w") as f:
        json.dump(story_dict, f, indent=4)

    # Print the location of the saved file
    print(f"\nStory saved to {filename}")
    story_end_time = time.time()
    total_story_time = story_end_time - start_time

    ##########################################################################
    ############################### 2 - Prompt Generator #####################
    ##########################################################################
    prompt_start_time = time.time()
    # Generate prompts for the sentences
    print("\nGenerating prompts for each sentence...")
    story_dict["sentences"] = split_story_into_sentences(
        story_dict.get("story", {}))
    sentences_with_prompts = generate_prompts_for_sentences(
        story_dict.get("sentences", {}), story_dict.get("story", {})
    )
    story_dict["sentences"] = sentences_with_prompts

     # Create thumbnail Prompt
    story_dict["youtube_details"]["thumbnail_prompt"] = generate_thumbnail_prompt(story_dict["youtube_details"]["youtube_title"], story_dict.get("story", {}))
    
    # Save the updated JSON file with prompts
    with open(filename, "w") as f:
        json.dump(story_dict, f, indent=4)

    print(f"Updated JSON with prompts saved to {filename}")

    prompt_end_time = time.time()
    total_prompt_time = prompt_end_time - prompt_start_time

    ##########################################################################
    ############################### 3 - Image Generator ######################
    ##########################################################################

    image_start_time = time.time()

    # Server and workflow configurations for image generation
    SERVER_ADDRESS = "127.0.0.1:8188"
    WORKFLOW_FILE = "flux_dev_space_example_16.json"
    SAVE_DIR = folder_name

    # # Generate images for the prompts
    # print("\nGenerating images for the prompts...")
    # generate_images_for_prompts(
    #     SERVER_ADDRESS,
    #     WORKFLOW_FILE,
    #     SAVE_DIR,
    #     story_dict.get("sentences", {}),
    #     timestamp,
    #     3
    # )
    # Generate images for the prompts
    print("\nGenerating images for the prompts...")
    
    generate_thumbnail(
        SERVER_ADDRESS,
        WORKFLOW_FILE,
        SAVE_DIR,
        story_dict["youtube_details"]["thumbnail_prompt"],
        timestamp,
        3,
    )

    generate_images_for_prompts(
        SERVER_ADDRESS,
        WORKFLOW_FILE,
        SAVE_DIR,
        story_dict.get("sentences", {}),
        timestamp,
        2,
    )



    # Define the final image output path
    final_image_folder = (
        f"E:\\ComfyUI_windows_portable\\ComfyUI\\output\\api\\{timestamp}"
    )
    story_dict["images_output"] = final_image_folder

    # Save the final JSON file with all outputs (prompts, audio, images)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(story_dict, f, indent=4)

    # print(f"Final JSON with all outputs saved to {filename}")

    image_end_time = time.time()
    total_image_time = image_end_time - image_start_time

    ##########################################################################
    ############################### 4 - Audio Generator ######################
    ##########################################################################
    audio_start_time = time.time()
    # Call the audio generation function using the folder path

    wav_path, mp3_path = generate_audio_from_json(
        folder_name, input_mp3=input_mp3_path)

    # Update the JSON file with the audio output path
    story_dict["audio_output"] = mp3_path
    with open(filename, "w") as f:
        json.dump(story_dict, f, indent=4)

    print(f"Generated audio files:\nWAV: {wav_path}\nMP3: {mp3_path}")

    audio_end_time = time.time()
    total_audio_time = audio_end_time - audio_start_time

    ##########################################################################
    ############################### 5 - Video Generator ######################
    ##########################################################################
    video_start_time = time.time()
    # Generate the final video
    print("\nGenerating final video...")
    video_output_folder = os.path.join(folder_name, "visix")
    final_video_output = os.path.join(folder_name, "final_story.mp4")
    audio_folder = os.path.join(folder_name, "verba")


    # generate_and_concatenate_videos(
    #     audio_base_path=audio_folder,
    #     images_base_path=final_image_folder,
    #     sentences=story_dict.get("sentences", {}),
    #     output_folder=video_output_folder,
    #     final_output_path=final_video_output,
    #     target_resolution=(1920, 1080),
    #     effect_type=None  # Set to None for random selection, or specify 'zoom_in', 'zoom_out', or 'pan'
    # )


    # Update the JSON with the video output path
    story_dict["video_output"] = final_video_output
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(story_dict, f, indent=4)
    generate_and_concatenate_videos(
        audio_base_path=audio_folder,
        images_base_path=final_image_folder,
        sentences=story_dict.get("sentences", {}),
        output_folder=video_output_folder,
        final_output_path=final_video_output,
        target_resolution=(1920, 1080),
        effect_type=None,
        # Set to None for random selection, or specify 'zoom_in', 'zoom_out',
        # or 'pan'
    )

    # Update the JSON with the video output path
    story_dict["video_output"] = final_video_output
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(story_dict, f, indent=4)

    print(f"Final video has been generated at {final_video_output}")
    print(f"Updated JSON with video paths saved to {filename}")

    video_end_time = time.time()
    total_video_time = video_end_time - video_start_time
    total_time = video_end_time - start_time

    ##########################################################################
    ###############################  Conclusion ##############################
    ##########################################################################
    print(
        f"\ntime taken to execute the story generation: {total_story_time:.2f} seconds"
    )
    print(
        f"\ntime taken to execute the prompt generation: {total_prompt_time:.2f} seconds"
    )
    print(
        f"\ntime taken to execute the audio generation: {total_audio_time:.2f} seconds"
    )
    print(
        f"\ntime taken to execute the image generation: {total_image_time:.2f} seconds"
    )
    print(
        f"\ntime taken to execute the video generation: {total_video_time:.2f} seconds"
    )
    print(f"\nTotal execution time: {total_time:.2f} seconds")
