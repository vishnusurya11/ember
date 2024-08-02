from moviepy.editor import ImageClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


# Create subtitle clip using PIL
def create_subtitle_clip(text, fontsize, color, size, duration, position, font_name):
    img = Image.new('RGBA', size, (0, 0, 0, 0))  # Fully transparent background
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype(f"{font_name.lower()}.ttf", fontsize)
    except IOError:
        print(f"unable to find the font --> {font_name.lower()} ")
        font = ImageFont.truetype("arial.ttf", fontsize)
        # font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Determine x position
    if position['x'] == 'center':
        text_x = (size[0] - text_width) // 2
    elif position['x'] == 'left':
        text_x = 10
    elif position['x'] == 'right':
        text_x = size[0] - text_width - 10
    else:
        text_x = (size[0] - text_width) // 2  # Default to center if not specified correctly

    # Determine y position
    if position['y'] == 'top':
        text_y = 10
    elif position['y'] == 'center':
        text_y = (size[1] - text_height) // 2
    elif position['y'] == 'bottom':
        text_y = size[1] - text_height - 10
    else:
        text_y = size[1] - text_height - 10  # Default to bottom if not specified correctly

    draw.text((text_x, text_y), text, font=font, fill=hex_to_rgb(color))
    
    txt_clip = ImageClip(np.array(img)).set_duration(duration)
    return txt_clip

# Add subtitles to the video
def add_subtitles(clip, subtitles):
    subtitle_clips = []
    for subtitle in subtitles:
        txt_clip = create_subtitle_clip(
            subtitle['text'],
            fontsize=subtitle.get('fontsize', 24),
            color=subtitle.get('color', '#FFFFFF'),  # Default to white,
            size=(clip.w, clip.h),
            duration=subtitle['end_time'] - subtitle['start_time'],
            position=subtitle['position'],
            font_name=subtitle.get('font', 'Arial')
        ).set_start(subtitle['start_time'])
        subtitle_clips.append(txt_clip)
    
    return CompositeVideoClip([clip] + subtitle_clips)
