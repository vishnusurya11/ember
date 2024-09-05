import os
import random
import subprocess
from tqdm import tqdm
import json

# TODO : add the zoom out affect


def create_video_for_sentence_ffmpeg(
        audio_path,
        image_folder,
        output_path,
        target_resolution="1080x1920",
        zoom_out=True):
    # Get all images in the folder that contain 'facefix' in the name
    images = [f for f in os.listdir(
        image_folder) if "facefix" in f and f.endswith(".png")]

    # Print how many images were found
    print(f"Found {len(images)} images in {image_folder}.")

    if not images:
        raise FileNotFoundError(f"No 'facefix' images found in {image_folder}")

    # Randomly pick one image
    selected_image = random.choice(images)
    image_path = os.path.join(image_folder, selected_image)

    # Print which image was selected
    print(f"Selected image: {selected_image}")

    # Construct the ffmpeg command with scaling and zoom-out for 9:16 aspect
    # ratio
    if zoom_out:
        zoom_filter = f"scale={target_resolution},zoompan=z='if(gte(zoom,1.5),zoom-0.005,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s={target_resolution}"
    else:
        zoom_filter = f"scale={target_resolution}"

    command = [
        "ffmpeg",
        "-y",  # Overwrite output files without asking
        "-loop",
        "1",  # Loop the image to match the audio duration
        "-i",
        image_path,  # Input image
        "-i",
        audio_path,  # Input audio
        "-vf",
        zoom_filter,  # Apply the zoom filter
        "-c:v",
        "libx264",  # Video codec
        "-c:a",
        "aac",  # Audio codec
        "-b:a",
        "192k",  # Audio bitrate
        "-pix_fmt",
        "yuv420p",  # Pixel format for compatibility
        "-shortest",  # Stop encoding when the shortest input ends
        output_path,  # Output file
    ]

    # Run the command
    subprocess.run(command, check=True)


def generate_and_concatenate_videos_ffmpeg(
    audio_base_path,
    images_base_path,
    sentences,
    output_folder,
    final_output_path,
    target_resolution="1080x1920",
    zoom_out=True,
):
    os.makedirs(output_folder, exist_ok=True)
    video_clips = []

    for key, value in tqdm(sentences.items(),
                           desc="Generating Videos for Sentences"):
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
            create_video_for_sentence_ffmpeg(
                audio_file,
                image_folder,
                output_video,
                target_resolution,
                zoom_out)
            video_clips.append(output_video)
        except Exception as e:
            print(f"Failed to create video for {key}: {e}")

    if video_clips:
        # Concatenate all video clips into one final video
        with open("file_list.txt", "w") as f:
            for clip in video_clips:
                f.write(f"file '{clip}'\n")

        command = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            "file_list.txt",
            "-c",
            "copy",
            final_output_path,
        ]
        subprocess.run(command, check=True)
        os.remove("file_list.txt")


if __name__ == "__main__":
    base_folder = r"E:\Ember\Ember\ember\data\20240904192910"

    # Load the story config to get the images_output_folder
    json_file = os.path.join(
        base_folder, f"codex_{os.path.basename(base_folder)}.json"
    )
    with open(json_file, "r", encoding="utf-8") as file:
        story_data = json.load(file)

    images_output_folder = story_data.get("images_output")
    audio_folder = os.path.join(base_folder, "verba")
    video_output_folder = os.path.join(base_folder, "visix")
    final_video_output = os.path.join(base_folder, "final_story.mp4")

    if not images_output_folder:
        raise ValueError(
            "images_output field not found in the JSON configuration.")

    # Generate videos for each sentence and concatenate them into a final video
    generate_and_concatenate_videos_ffmpeg(
        audio_folder,
        images_output_folder,
        story_data.get("sentences", {}),
        video_output_folder,
        final_video_output,
        target_resolution="1080x1920",
        zoom_out=True,
    )

    # Update the JSON with the video output path
    story_data["video_output"] = final_video_output
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(story_data, file, indent=4)

    print(f"Final video has been generated at {final_video_output}")
    print(f"Updated JSON with video paths saved to {json_file}")
