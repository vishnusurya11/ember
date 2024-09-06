import os
import random
import json
from tqdm import tqdm
import moviepy.editor as mp
import math
from PIL import Image
import numpy as np

def zoom_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size
        new_size = [
            math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
            math.ceil(img.size[1] * (1 + (zoom_ratio * t)))
        ]
        new_size[0] = new_size[0] + (new_size[0] % 2)
        new_size[1] = new_size[1] + (new_size[1] % 2)
        img = img.resize(new_size, Image.LANCZOS)
        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)
        img = img.crop([x, y, new_size[0] - x, new_size[1] - y]).resize(base_size, Image.LANCZOS)
        result = np.array(img)
        img.close()
        return result
    return clip.fl(effect)

def pan_effect(clip, pan_ratio, direction):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size
        
        if direction in ['left', 'right']:
            new_width = math.ceil(base_size[0] / (1 - pan_ratio))
            new_size = (new_width, base_size[1])
        else:  # 'up' or 'down'
            new_height = math.ceil(base_size[1] / (1 - pan_ratio))
            new_size = (base_size[0], new_height)
        
        img = img.resize(new_size, Image.LANCZOS)
        
        if direction == 'right':
            x = int((new_size[0] - base_size[0]) * (t / clip.duration))
            y = 0
        elif direction == 'left':
            x = int((new_size[0] - base_size[0]) * (1 - t / clip.duration))
            y = 0
        elif direction == 'down':
            x = 0
            y = int((new_size[1] - base_size[1]) * (t / clip.duration))
        else:  # 'up'
            x = 0
            y = int((new_size[1] - base_size[1]) * (1 - t / clip.duration))
        
        img = img.crop([x, y, x + base_size[0], y + base_size[1]])
        
        result = np.array(img)
        img.close()
        return result
    return clip.fl(effect)

def create_video_for_sentence(audio_path, image_folder, output_path, target_resolution=(1920, 1080), effect_type=None, effect_ratio=0.06):
    # Get all images in the folder that contain 'facefix' in the name
    images = [f for f in os.listdir(image_folder) if "facefix" in f and f.endswith(".png")]

    if not images:
        raise FileNotFoundError(f"No 'facefix' images found in {image_folder}")

    # Randomly pick one image
    selected_image = random.choice(images)
    image_path = os.path.join(image_folder, selected_image)

    # Create the base clip
    audio_clip = mp.AudioFileClip(audio_path)
    image_clip = mp.ImageClip(image_path).set_duration(audio_clip.duration).resize(target_resolution)

    # If effect_type is not specified, choose randomly
    if effect_type is None:
        effect_type = random.choice(['zoom_in', 'zoom_out', 'pan'])

    # Apply effect
    if effect_type == 'zoom_in':
        effected_clip = zoom_effect(image_clip, effect_ratio)
    elif effect_type == 'zoom_out':
        effected_clip = zoom_effect(image_clip, effect_ratio).fx(mp.vfx.time_mirror)
    elif effect_type == 'pan':
        direction = random.choice(['left', 'right', 'up', 'down'])
        effected_clip = pan_effect(image_clip, effect_ratio, direction)
    else:
        raise ValueError("effect_type must be 'zoom_in', 'zoom_out', 'pan', or None")

    # Combine video and audio
    final_clip = effected_clip.set_audio(audio_clip)

    # Write the output
    final_clip.write_videofile(output_path, fps=30)

def generate_and_concatenate_videos(audio_base_path, images_base_path, sentences, output_folder, final_output_path, target_resolution=(1920, 1080), effect_type=None):
    os.makedirs(output_folder, exist_ok=True)
    video_clips = []

    for key, value in tqdm(sentences.items(), desc="Generating Videos for Sentences"):
        audio_file = os.path.join(audio_base_path, f"{key}.wav")
        image_folder = os.path.join(images_base_path, key)

        if not os.path.exists(audio_file):
            print(f"Audio file {audio_file} does not exist, skipping.")
            continue

        if not os.path.exists(image_folder):
            print(f"Image folder {image_folder} does not exist, skipping.")
            continue

        output_video = os.path.join(output_folder, f"{key}.mp4")

        try:
            create_video_for_sentence(audio_file, image_folder, output_video, target_resolution, effect_type)
            video_clips.append(mp.VideoFileClip(output_video))
        except Exception as e:
            print(f"Failed to create video for {key}: {e}")

    if video_clips:
        # Concatenate all video clips into one final video
        final_clip = mp.concatenate_videoclips(video_clips)
        final_clip.write_videofile(final_output_path, fps=30)

if __name__ == "__main__":
    base_folder = r"E:\Ember\Ember\ember\data\20240904192910"

    # Load the story config to get the images_output_folder
    json_file = os.path.join(base_folder, f"codex_{os.path.basename(base_folder)}.json")
    with open(json_file, "r", encoding="utf-8") as file:
        story_data = json.load(file)

    images_output_folder = story_data.get("images_output")
    audio_folder = os.path.join(base_folder, "verba")
    video_output_folder = os.path.join(base_folder, "visix")
    final_video_output = os.path.join(base_folder, "final_story.mp4")

    if not images_output_folder:
        raise ValueError("images_output field not found in the JSON configuration.")

    # Generate videos for each sentence and concatenate them into a final video
    generate_and_concatenate_videos(
        audio_folder,
        images_output_folder,
        story_data.get("sentences", {}),
        video_output_folder,
        final_video_output,
        target_resolution=(1920, 1080),
        effect_type=None  # Set to None for random selection, or specify 'zoom_in', 'zoom_out', or 'pan'
    )

    # Update the JSON with the video output path
    story_data["video_output"] = final_video_output
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(story_data, file, indent=4)

    print(f"Final video has been generated at {final_video_output}")
    print(f"Updated JSON with video paths saved to {json_file}")