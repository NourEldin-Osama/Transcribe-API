import torch
from transformers import pipeline
import os

# Initialize the Whisper model
task = "automatic-speech-recognition"
model_name = "openai/whisper-large-v3"  # Adjust model if necessary
device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = pipeline(task=task, model=model_name, device=device)

async def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribe an audio file using Whisper.
    """
    # Check if the audio file exists
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

    # Run the transcription using the model
    transcription = pipe(audio_file_path, chunk_length_s=30, batch_size=24, return_timestamps=False)

    # Return the text
    return transcription["text"]
