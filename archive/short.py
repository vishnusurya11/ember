import yaml
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, AudioFileClip
from PIL import Image
import numpy as np
import os
from subtitles import add_subtitles

# Load template from YAML file
def load_template(template_path):
    with open(template_path, 'r') as file:
        return yaml.safe_load(file)

# Custom resize function using PIL
def custom_resize(clip, newsize):
    def resize_frame(frame):
        img = Image.fromarray(frame)
        img = img.resize(newsize, Image.LANCZOS)
        return np.array(img)
    return clip.fl_image(resize_frame)

# Ensure 9:16 aspect ratio
def ensure_aspect_ratio(clip, target_aspect_ratio=(9, 16)):
    iw, ih = clip.size
    target_w, target_h = target_aspect_ratio
    
    # Calculate the new dimensions
    if iw/ih > target_w/target_h:  # If the video is too wide
        new_w = ih * target_w / target_h
        new_h = ih
    else:  # If the video is too tall
        new_w = iw
        new_h = iw * target_h / target_w

    # Center crop the video to the new dimensions
    clip = clip.crop(width=new_w, height=new_h, x_center=iw/2, y_center=ih/2)
    return clip

# Create video template
def create_video_template(template):
    # Load video clips
    clips = [custom_resize(ensure_aspect_ratio(VideoFileClip(file['path'])), (1080, 1920)) for file in template['input_video_files']]
    
    # Concatenate video clips
    final_clip = concatenate_videoclips(clips, method="compose")

    # Add audio and set the final video length to match the audio length
    if 'input_audio_file' in template and os.path.exists(template['input_audio_file']):
        audio_clip = AudioFileClip(template['input_audio_file'])
        final_clip = final_clip.set_audio(audio_clip)
        final_clip = final_clip.set_duration(audio_clip.duration)
    
    # Add subtitles
    if 'subtitles' in template:
        final_clip = add_subtitles(final_clip, template['subtitles'])
    
    # Write the result to a file
    final_clip.write_videofile(template['output_video_file'], codec="libx264", fps=24)

if __name__ == "__main__":
    template = load_template("templates/template_short.yaml")
    create_video_template(template)
