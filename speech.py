import torch
from TTS.api import TTS
from pydub import AudioSegment
import datetime
import os
import numpy as np

"""
https://github.com/coqui-ai/TTS
https://librivox.org/search

"""

# Initial setup
input_mp3 = "sample_4.mp3"
sample_input = "sample_input.wav"
device = "cuda" if torch.cuda.is_available() else "cpu"

# Convert MP3 to WAV for speaker embedding
audio = AudioSegment.from_mp3(input_mp3)
audio.export(sample_input, format="wav")
print(f"Converted '{input_mp3}' to '{sample_input}' successfully.")

# Initialize TTS
# tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)


# Assuming TTS is defined and working
# model_manager = TTS().list_models()
#
# # Open a file named 'output.txt' in write mode with UTF-8 encoding
# with open('output.txt', 'w', encoding='utf-8') as file:
#     file.write(str(model_manager) + '\n')  # Write the string representation of model_manager to file
#     for attribute in dir(model_manager):
#         # Filter out special methods and properties (those starting with '__')
#         if not attribute.startswith('__'):
#             # Get the value of each attribute
#             value = getattr(model_manager, attribute)
#             # Create a string that combines the attribute and its value
#             attribute_string = f"{attribute}: {value}\n"
#             # Write the attribute string to the file
#             file.write(attribute_string)

#     # Write a separator line
#     file.write("--------------------------------------------\n")


# Input text, stripping leading/trailing whitespace
text_input = """
Host: "Welcome to 'Narrative Nexus,' where the boundaries of time, space, and fiction are merely guidelines! I'm Victor Stone, and tonight, we're chatting with The Boy Who Lived, Harry Potter. Harry, it’s your first time on the show—welcome!"

Guest: "Thanks, Victor. It’s great to be here."

Host: "So, Harry, you’ve just finished your first year at Hogwarts. How was it adjusting from life with the Dursleys to life at a magical school?"

Guest: "It’s been amazing! I went from being stuck in a cupboard to flying on a broomstick and learning spells. It’s like a dream come true."

Host: "That’s quite a change! I hear you had a bit of an adventure with a three-headed dog and a giant chessboard. How did you manage that?"

Guest: "Oh, that was intense! But with Hermione and Ron by my side, we made it through. It’s all about teamwork."

Host: "Teamwork, indeed. Speaking of adventures, any thoughts on what next year might bring? Maybe a bit more peace and quiet?"

Guest: laughs "I really hope so! A quiet year would be nice after all that excitement."

Host: "I’m sure you’ll get that quiet year... or not. Hogwarts does have a way of keeping things interesting, doesn’t it?"

Guest: "Yeah, I guess it does. But I’m still hoping for a bit of calm."

Host: "Wise beyond your years, Harry. But don’t worry, I’m sure nothing too crazy will happen in the next few years... maybe just a giant snake or two."

Guest: "A giant snake? You're joking, right?"

Host: "Oh, just a hunch. Anyway, I hear you’ve become quite the Quidditch star. How does it feel to be the youngest Seeker in a century?"

Guest: "It’s incredible! I never thought I’d be good at flying, but it turns out I have a knack for it."

Host: "You certainly do. Just wait until you try catching the Golden Snitch with a broken arm—that’ll be a story for the ages."

Guest: "A broken arm? That sounds painful."

Host: "Let’s hope it doesn’t come to that. So, any plans for the summer holidays? Maybe a bit of rest and relaxation?"

Guest: "Well, I’ll be going back to the Dursleys, so probably not much of that. But I’m looking forward to coming back to Hogwarts."

Host: "Ah, the Dursleys. Well, enjoy your summer as best as you can. Any final thoughts before we wrap up?"

Guest: "Just that I can’t wait to see what happens next. Hogwarts is full of surprises!"

Host: "Indeed it is. Thanks for joining us, Harry. That’s all for tonight on 'Narrative Nexus.' Stay tuned for more magical conversations!"

Guest: "Thanks, Victor!"
"""
text_input = text_input.strip()

# Directory setup with sanitized subfolder name
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
# Sanitize subfolder_name to remove non-alphanumeric characters except for
# underscores and spaces
sanitized_text = (
    "".join(c if c.isalnum() or c in [" ", "_"] else "" for c in text_input[:10])
    .strip()
    .replace(" ", "_")
)
subfolder_name = f"{timestamp}_{sanitized_text}"
data_folder = os.path.join("data", subfolder_name)
audiolist_folder = os.path.join(data_folder, "audiolist")
os.makedirs(audiolist_folder, exist_ok=True)

# Split the text by sentences
sentences = [
    sentence.strip() + "." for sentence in text_input.split(".") if sentence.strip()
]

length_sen = len(sentences)

# Process each sentence and save audio files
for i, sentence in enumerate(sentences):
    file_path = os.path.join(audiolist_folder, f"audio_{i+1:03d}.wav")
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
    # tts = TTS("tts_models/multilingual/multi-dataset/bark").to(device)
    wav = tts.tts(text=sentence, speaker_wav=sample_input, language="en")
    tts.tts_to_file(
        text=sentence, speaker_wav=sample_input, language="en", file_path=file_path
    )
    print(f"Generated audio for sentence {i+1}/{length_sen}")

# Combine audio files
combined_audio = AudioSegment.empty()
for i in range(len(sentences)):
    file_path = os.path.join(audiolist_folder, f"audio_{i+1:03d}.wav")
    sentence_audio = AudioSegment.from_wav(file_path)
    combined_audio += sentence_audio

# Save the combined audio to the main data folder
final_path = os.path.join(data_folder, "final.wav")
combined_audio.export(final_path, format="wav")
print(f"Combined audio saved to {final_path}")
