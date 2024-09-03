import torch
from TTS.api import TTS
from pydub import AudioSegment
import os
import json
from datetime import datetime

def generate_audio_from_json(json_file_path, input_mp3='sample_4.mp3'):
    # Initial setup
    sample_input = 'sample_input.wav'
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Convert MP3 to WAV for speaker embedding
    audio = AudioSegment.from_mp3(input_mp3)
    audio.export(sample_input, format='wav')
    print(f"Converted '{input_mp3}' to '{sample_input}' successfully.")

    # Load the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        story_data = json.load(file)

    # Directory setup with sanitized subfolder name
    timestamp = datetime.now().strftime('%Y%m%d%H%M')
    subfolder_name = f"{timestamp}_story_audio"
    data_folder = os.path.join('data', subfolder_name)
    audiolist_folder = os.path.join(data_folder, 'audiolist')
    os.makedirs(audiolist_folder, exist_ok=True)

    # Process each sentence and save audio files
    sentences = story_data.get('sentences', {})
    combined_audio = AudioSegment.empty()

    for key, value in sentences.items():
        sentence = value.get('sentence', '').strip()
        if not sentence:
            continue  # Skip if the sentence is empty

        file_path = os.path.join(audiolist_folder, f"{key}.wav")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        wav = tts.tts(text=sentence, speaker_wav=sample_input, language="en")
        tts.tts_to_file(text=sentence, speaker_wav=sample_input, language="en", file_path=file_path)
        print(f"Generated audio for sentence {key}")

        # Combine the sentence audio into a single file
        sentence_audio = AudioSegment.from_wav(file_path)
        combined_audio += sentence_audio

    # Save the combined audio to the main data folder
    final_path = os.path.join(data_folder, "final.wav")
    combined_audio.export(final_path, format="wav")
    print(f"Combined audio saved to {final_path}")

    # Optionally, convert the final WAV file to MP3
    final_mp3_path = os.path.join(data_folder, "final.mp3")
    combined_audio.export(final_mp3_path, format="mp3")
    print(f"Combined audio saved as MP3 to {final_mp3_path}")
    
    return final_path, final_mp3_path

if __name__ == "__main__":
    # Define the path to your JSON file and input MP3 file
    json_file_path = 'data/script_20240902172708.json'
    input_mp3_path = 'sample_4.mp3'

    # Call the function to generate audio from the JSON file
    wav_path, mp3_path = generate_audio_from_json(json_file_path, input_mp3=input_mp3_path)

    print(f"Generated audio files:\nWAV: {wav_path}\nMP3: {mp3_path}")
