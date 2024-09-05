import torch
from TTS.api import TTS
from pydub import AudioSegment
import os
import json
from datetime import datetime


def generate_audio_from_json(folder_path, input_mp3="sample_5.mp3"):
    # Initial setup
    sample_input = "sample_input.wav"
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Convert MP3 to WAV for speaker embedding
    audio = AudioSegment.from_mp3(input_mp3)
    audio.export(sample_input, format="wav")
    print(f"Converted '{input_mp3}' to '{sample_input}' successfully.")

    # Find the JSON file in the given folder
    json_file_path = None
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            json_file_path = os.path.join(folder_path, file_name)
            break

    if not json_file_path:
        raise FileNotFoundError("No JSON file found in the provided folder.")

    # Load the JSON file
    with open(json_file_path, "r", encoding="utf-8") as file:
        story_data = json.load(file)

    # Directory setup for audio list within the provided folder
    audiolist_folder = os.path.join(folder_path, "audiolist")
    os.makedirs(audiolist_folder, exist_ok=True)

    # Process each sentence and save audio files
    sentences = story_data.get("sentences", {})
    combined_audio = AudioSegment.empty()

    for key, value in sentences.items():
        sentence = value.get("sentence", "").strip()
        if not sentence:
            continue  # Skip if the sentence is empty

        file_path = os.path.join(audiolist_folder, f"{key}.wav")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        wav = tts.tts(text=sentence, speaker_wav=sample_input, language="en")
        tts.tts_to_file(
            text=sentence,
            speaker_wav=sample_input,
            language="en",
            file_path=file_path)
        print(f"Generated audio for sentence {key}")

        # Combine the sentence audio into a single file
        sentence_audio = AudioSegment.from_wav(file_path)
        combined_audio += sentence_audio

    # Save the combined audio to the provided folder
    final_path = os.path.join(folder_path, "final_audio.wav")
    combined_audio.export(final_path, format="wav")
    print(f"Combined audio saved to {final_path}")

    # Optionally, convert the final WAV file to MP3
    final_mp3_path = os.path.join(folder_path, "final_audio.mp3")
    combined_audio.export(final_mp3_path, format="mp3")
    print(f"Combined audio saved as MP3 to {final_mp3_path}")

    # Update the JSON config with the final MP3 path
    story_data["audio_output"] = final_mp3_path
    with open(json_file_path, "w", encoding="utf-8") as file:
        json.dump(story_data, file, indent=4)
    print(f"Updated JSON config with final MP3 path: {final_mp3_path}")

    return final_path, final_mp3_path


if __name__ == "__main__":
    # Define the high-level folder path where the JSON file is located
    folder_path = "E:\\Ember\\Ember\\ember\\data\\20240902180118\\"
    input_mp3_path = "sample_5.mp3"

    # Call the function to generate audio from the JSON file
    wav_path, mp3_path = generate_audio_from_json(
        folder_path, input_mp3=input_mp3_path)

    print(f"Generated audio files:\nWAV: {wav_path}\nMP3: {mp3_path}")
