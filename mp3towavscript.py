import os
import subprocess

def convert_mp3_to_wav(input_folder, output_folder):
    """
    Converts all MP3 files in the input folder to WAV files in the output folder.

    Args:
        input_folder (str): Path to the folder containing MP3 files.
        output_folder (str): Path to the folder where WAV files will be saved.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".mp3"):
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + ".wav"
            output_path = os.path.join(output_folder, output_filename)

            try:
                # Use ffmpeg to convert MP3 to WAV
                subprocess.run(
                    ['ffmpeg', '-i', input_path, output_path],
                    check=True,
                    capture_output=True,
                    text=True
                )
                print(f"Converted: {filename} -> {output_filename}")
            except subprocess.CalledProcessError as e:
                print(f"Error converting {filename}: {e.stderr}")
            except FileNotFoundError:
                print("Error: ffmpeg not found. Make sure ffmpeg is installed and in your PATH.")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break

if __name__ == "__main__":
    input_folder = "/Users/mikesidnam/Desktop/morphagene"  # Targeted input folder
    output_folder = "/Users/mikesidnam/Desktop/morphagene"  # Targeted output folder

    convert_mp3_to_wav(input_folder, output_folder)
