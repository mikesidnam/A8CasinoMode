import os
from pydub import AudioSegment

# Directories
INPUT_DIR = "/Users/mikesidnam/Desktop/Keepers/NormalizedKeepers"
OUTPUT_DIR = "/Users/mikesidnam/Desktop/EditedKeepers"

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Parameters for silence detection
SILENCE_THRESHOLD = -35  # dBFS (anything below this is considered silence)
MIN_SILENCE_LEN = 100  # milliseconds (minimum length of silence to detect)


def strip_leading_silence(input_path, output_path):
    # Load the WAV file
    audio = AudioSegment.from_wav(input_path)

    # Detect leading silence
    silence_end = audio.detect_leading_silence(
        silence_threshold=SILENCE_THRESHOLD,
        chunk_size=MIN_SILENCE_LEN
    )

    # If no silence detected, silence_end is 0; otherwise