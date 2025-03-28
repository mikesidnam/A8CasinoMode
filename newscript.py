import os
import random
import yaml
from dotenv import load_dotenv
from elevenlabs import ElevenLabs
from pydub import AudioSegment
from collections import defaultdict

# Load .env file
load_dotenv()

# Retrieve API Key
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY is missing. Set it in your .env file or environment variables.")

# Initialize ElevenLabs client
client = ElevenLabs(api_key=API_KEY)

# Directories
SAMPLES_DIR = "/Users/mikesidnam/Desktop/samples/11api/1"
OUTPUT_DIR = "/Users/mikesidnam/Desktop/samples/11api/1/presets"
NUM_PRESETS = 4
CHANNELS_PER_PRESET = 8
SAMPLES_PER_CHANNEL = 8

# Ensure directories exist
os.makedirs(SAMPLES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# List of prompts (expand as needed, minimum 64 for unique samples per preset)
prompts = [
    "Bell alarm in the distance",
    "Droning low pitched hum",
    "Soft female speech whisper",
    "Electromagnetic interference",
    "Tube bells chiming softly",
    "Sine wave oscillating slowly",
    "CD skipping glitch sound",
    "Air raid siren far away",
    "Gentle wind through trees",
    "Metallic clank echoing",
    "Distant thunderstorm rumble",
    "High-pitched electronic beep",
    "Crackling fire embers",
    "Ocean waves crashing lightly",
    "Bird chirping in forest",
    "Mechanical whirring noise",
    "Echoing footsteps in hall",
    "Faint radio static noise",
    "Water dripping in cave",
    "Wind chimes in breeze",
    "Old clock ticking loudly",
    "Distant train whistle",
    "Rustling leaves in wind",
    "Low rumble of machinery",
    "Flickering fluorescent buzz",
    "Creaking wooden floor",
    "Subtle heartbeat pulse",
    "Chirping crickets at night",
    "Hiss of steam escaping",
    "Tapping on glass window",
    "Muffled voices through wall",
    "Slow piano note decay",
    "Gentle rain on rooftop",
    "Buzzing of electric current",
    "Faint owl hooting",
    "Rattling of loose chains",
    "Distant foghorn blast",
    "Soft guitar string pluck",
    "Whistling wind through gap",
    "Crunching gravel footsteps",
    "Low drone of airplane",
    "Ticking metronome sound",
    "Echoing drip in tunnel",
    "Faint laughter in distance",
    "Squeaking rusty hinge",
    "Humming of refrigerator",
    "Chiming of small bell",
    "Distant dog barking",
    "Rustling of paper pages",
    "Clatter of falling coins",
    "Whir of spinning fan",
    "Popping of bubble wrap",
    "Sizzling of frying pan",
    "Clicking of typewriter",
    "Distant car horn honk",
    "Soft thud of dropped book",
    "Hiss of aerosol spray",
    "Tinkle of breaking glass",
    "Rumble of rolling thunder",
    "Squeal of braking tires",
    "Chugging of old engine",
    "Patter of running feet",
    "Buzz of flying insect",
    "Clang of metal striking"
]

# Exact durations for each sample (in seconds, adjust as needed)
durations = [10, 8, 12, 6, 10, 8, 12, 6]  # 8 durations, one per sample in a bank


# Generate banks of 8 samples, ensuring uniqueness per channel
def generate_sample_banks(num_presets):
    sample_banks = []
    used_prompts = set()
    total_samples_needed = num_presets * CHANNELS_PER_PRESET * SAMPLES_PER_CHANNEL

    if len(prompts) < total_samples_needed:
        print(f"Warning: Only {len(prompts)} prompts available, need {total_samples_needed}. Duplicates will occur.")

    for preset_idx in range(num_presets):
        preset_banks = []
        for channel_idx in range(CHANNELS_PER_PRESET):
            bank_samples = []
            available_prompts = [p for p in prompts if p not in used_prompts]

            # If not enough unique prompts, reuse randomly
            if len(available_prompts) < SAMPLES_PER_CHANNEL:
                available_prompts = prompts.copy()

            random.shuffle(available_prompts)
            bank_prompts = available_prompts[:SAMPLES_PER_CHANNEL]

            for idx, prompt in enumerate(bank_prompts):
                duration = durations[idx]
                output_base = f"sound_p{preset_idx + 1}_c{channel_idx + 1}_{idx + 1}"
                output_mp3 = os.path.join(SAMPLES_DIR, f"{output_base}.mp3")
                output_wav = os.path.join(SAMPLES_DIR, f"{output_base}.wav")

                # Skip if WAV already exists to avoid regenerating
                if os.path.exists(output_wav):
                    bank_samples.append(os.path.basename(output_wav))
                    continue

                print(f"Generating: {prompt} ({duration}s) -> {output_wav}")
                audio_generator = client.text_to_sound_effects.convert(
                    text=prompt,
                    duration_seconds=duration
                )
                audio_bytes = b"".join(audio_generator)

                # Save as MP3 first
                with open(output_mp3, "wb") as f:
                    f.write(audio_bytes)

                # Convert to WAV (default ElevenLabs sample rate, e.g., 44.1kHz)
                audio = AudioSegment.from_mp3(output_mp3)
                audio.export(output_wav, format="wav")
                os.remove(output_mp3)  # Remove temporary MP3

                bank_samples.append(os.path.basename(output_wav))
                used_prompts.add(prompt)

            preset_banks.append(bank_samples)
        sample_banks.append(preset_banks)

    return sample_banks


# Generate samples for all presets (64 unique samples per preset)
sample_banks = generate_sample_banks(NUM_PRESETS)


# Custom YAML dumper to remove quotes
class NoQuotesDumper(yaml.SafeDumper):
    def represent_str(self, data):
        return self.represent_scalar('tag:yaml.org,2002:str', data, style='')


NoQuotesDumper.add_representer(str, NoQuotesDumper.represent_str)

# Exact working Preset 15 as boilerplate (unchanged)
preset_template = {
    "Preset 15 ": {
        "Name ": "New",
        "XfadeACV ": "1B",
        "XfadeAWidth ": "5.00",
        "Channel 1 ": {
            "PlayMode ": 1,
            "LinFM ": "2A 1.00",
            "PitchCV ": "2B 0.50",
            "PMIndexMod ": "2A 1.00",
            "PanMod ": "2C 1.00",
            "XfadeGroup ": "A",
            "ZonesCV ": "1C",
            "Zone 1 ": {"Sample ": "11L-Air_raid_siren_dista-1742491271673.wav", "MinVoltage ": "+4.52"},
            "Zone 2 ": {"Sample ": "11L-cd_skipping_stereo_g-1742491458253.wav", "MinVoltage ": "+4.00"},
            "Zone 3 ": {"Sample ": "11L-electromagnetic_micr-1742491383913.wav", "MinVoltage ": "+3.54"},
            "Zone 4 ": {"Sample ": "11L-The_Bobolink-1742491322488.wav", "MinVoltage ": "+3.00"},
            "Zone 5 ": {"Sample ": "11L-tube_bells-1742491266689.wav", "Side ": 1, "MinVoltage ": "+2.50"},
            "Zone 6 ": {"Sample ": "11L-sine_wave-1742491298615.wav", "MinVoltage ": "+1.99"},
            "Zone 7 ": {"Sample ": "11L-soft_female_speech_a-1742491275400.wav", "Side ": 1, "MinVoltage ": "+1.43"},
            "Zone 8 ": {"Sample ": "11L-tube_bells-1742491266689.wav", "Side ": 1, "MinVoltage ": "-5.00"}
        },
        "Channel 2 ": {
            "PlayMode ": 1,
            "LinFM ": "2A 1.00",
            "PitchCV ": "2B 0.50",
            "PMIndexMod ": "2A 1.00",
            "PanMod ": "2C 1.00",
            "XfadeGroup ": "A",
            "ZonesCV ": "1C",
            "Zone 1 ": {"Sample ": "11L-Air_raid_siren_dista-1742491271673.wav", "MinVoltage ": "+4.52"},
            "Zone 2 ": {"Sample ": "11L-cd_skipping_stereo_g-1742491458253.wav", "MinVoltage ": "+4.00"},
            "Zone 3 ": {"Sample ": "11L-electromagnetic_micr-1742491383913.wav", "MinVoltage ": "+3.54"},
            "Zone 4 ": {"Sample ": "11L-The_Bobolink-1742491322488.wav", "MinVoltage ": "+3.00"},
            "Zone 5 ": {"Sample ": "11L-tube_bells-1742491266689.wav", "Side ": 1, "MinVoltage ": "+2.50"},
            "Zone 6 ": {"Sample ": "11L-sine_wave-1742491298615.wav", "MinVoltage ": "+1.99"},
            "Zone 7 ": {"Sample ": "11L-soft_female_speech_a-1742491275400.wav", "Side ": 1, "MinVoltage ": "+1.43"},
            "Zone 8 ": {"Sample ": "11L-tube_bells-1742491266689.wav", "Side ": 1, "MinVoltage ": "-5.00"}
        },
        "Channel 3 ": {
            "PlayMode ": 1,
            "LinFM ": "2A 1.00",
            "PitchCV ": "2B 0.50",
            "PMIndexMod ": "2A 1.00",
            "PanMod ": "2C 1.00",
            "XfadeGroup ": "A",
            "ZonesCV ": "1C",
            "Zone 1 ": {"Sample ": "11L-Air_raid_siren_dista-1742491271673.wav", "MinVoltage ": "+4.52"},
            "Zone 2 ": {"Sample ": "11L-cd_skipping_stereo_g-1742491458253.wav", "MinVoltage ": "+4.00"},
            "Zone 3 ": {"Sample ": "11L-electromagnetic_micr-1742491383913.wav", "MinVoltage ": "+3.54"},
            "Zone 4 ": {"Sample ": "11L-The_Bobolink-1742491322488.wav", "MinVoltage ": "+3.00"},
            "Zone 5 ": {"Sample ": "11L-tube_bells-1742491266689.wav", "Side ": 1, "MinVoltage ": "+2.50"},
            "Zone 6 ": {"Sample ": "11L-sine_wave-1742491298615.wav", "MinVoltage ": "+1.99"},
            "Zone 7 ": {"Sample ": "11L-soft_female_speech_a-1742491275400.wav", "Side ": 1, "MinVoltage ": "+1.43"},
            "Zone 8 ": {"Sample ": "11L-tube_bells-1742491266689.wav", "Side ": 1, "MinVoltage ": "-5.00"}
        },
        "Channel 4 ": {
            "PlayMode ": 1,
            "LinFM ": "2A 1.00",
            "PitchCV ": "2B 0.50",
            "PMIndexMod ": "2A 1.00",
            "PanMod ": "2C 1.00",
            "XfadeGroup ": "A",
            "ZonesCV ": "1C",
            "Zone 1 ": {"Sample ": "11L-Air_raid_siren_dista-1742491271673.wav", "MinVoltage ": "+4.52"},
            "Zone 2 ": {"Sample ": "11L-cd_skipping_stereo_g-1742491458253.wav", "MinVoltage ": "+4.00"},
            "Zone 3 ": {"Sample ": "11L-electromagnetic_micr-1742491383913.wav", "MinVoltage ": "+3.54"},
            "Zone 4 ": {"Sample ": "11L-The_Bobolink-1742491322488.wav", "MinVoltage ": "+3.00"},
            "Zone 5 ": {"Sample ": "11L-tube_bells-1742491266689.wav", "Side ": 1, "MinVoltage ": "+2.50"},
            "Zone 6 ": {"Sample ": "11L-sine_wave-1742491298615.wav", "MinVoltage ": "+1.99"},
            "Zone 7 ": {"Sample ": "11L-soft_female_speech_a-1742491275400.wav", "Side ": 1, "MinVoltage ": "+1.43"},
            "Zone 8 ": {"Sample ": "11L-tube_bells-1742491266689.wav", "Side ": 1, "MinVoltage ": "-5.00"}
        },
        "Channel 5 ": {
            "PlayMode ": 1,
            "LinFM ": "2A 1.00",
            "PitchCV ": "2B 0.50",
            "PMIndexMod ": "2A 1.00",
            "PanMod ": "2C 1.00",
            "XfadeGroup ": "A",
            "ZonesCV ": "1C",
            "Zone 1 ": {"Sample ": "11L-Air_raid_siren_dista-1742491271673.wav", "MinVoltage ": "+4.52"},
            "Zone 2 ": {"Sample ": "11L-cd_skipping_stereo_g-1742491458253.wav", "MinVoltage ": "+4.00"},
            "Zone 3 ": {"Sample ": "11L-electromagnetic_micr-1742491383913.wav", "MinVoltage ": "+3.54"},
            "Zone 4 ": {"Sample ": "11L-The_Bobolink-1742491322488.wav", "MinVoltage ": "+3.00"},
            "Zone 5 ": {"Sample ": "11L-tube_bells-1742491266689.wav", "Side ": 1, "MinVoltage ": "+2.50"},
            "Zone 6 ": {"Sample ": "11L-sine_wave-1742491298615.wav", "MinVoltage ": "+1.99"},
            "Zone 7 ": {"Sample ": "11L-soft_female_speech_a-1742491275400.wav", "Side ": 1, "MinVoltage ": "+1.43"},
            "Zone 8 ": {"Sample ": "11L-tube_bells-1742491266689.wav", "Side ": 1, "MinVoltage ": "-5.00"}
        },
        "Channel 6 ": {
            "PlayMode ": 1,
            "LinFM ": "2A 1.00",
            "PitchCV ": "2B 0.50",
            "PMIndexMod ": "2A 1.00",
            "PanMod ": "2C 1.00",
            "XfadeGroup ": "A",
            "ZonesCV ": "1C",
            "Zone 1 ": {"Sample ": "11L-Air_raid_siren_dista-1742491271673.wav", "MinVoltage ": "+4.52"},
            "Zone 2 ": {"Sample ": "11L-cd_skipping_stereo_g-1742491458253.wav", "MinVoltage ": "+4.00"},
            "Zone 3 ": {"Sample ": "11L-electromagnetic_micr-1742491383913.wav", "MinVoltage ": "+3.54"},
            "Zone 4 ": {"Sample ": "11L-The_Bobolink-1742491322488.wav", "MinVoltage ": "+3.00"},
            "Zone 5 ": {"Sample ": "11L-tube_bells-1742491266689.wav", "Side ": 1, "MinVoltage ": "+2.50"},
            "Zone 6 ": {"Sample ": "11L-sine_wave-1742491298615.wav", "MinVoltage ": "+1.99"},
            "Zone 7 ": {"Sample ": "11L-soft_female_speech_a-1742491275400.wav", "Side ": 1, "MinVoltage ": "+1.43"},
            "Zone 8 ": {"Sample ": "11L-tube_bells-1742491266689.wav", "Side ": 1, "MinVoltage ": "-5.00"}
        },
        "Channel 7 ": {
            "PlayMode ": 1,
            "LinFM ": "2A 1.00",
            "PitchCV ": "2B 0.50",
            "PMIndexMod ": "2A 1.00",
            "PanMod ": "2C 1.00",
            "XfadeGroup ": "A",
            "ZonesCV ": "1C",
            "Zone 1 ": {"Sample ": "11L-Air_raid_siren_dista-1742491271673.wav", "MinVoltage ": "+4.52"},
            "Zone 2 ": {"Sample ": "11L-cd_skipping_stereo_g-1742491458253.wav", "MinVoltage ": "+4.00"},
            "Zone 3 ": {"Sample ": "11L-electromagnetic_micr-1742491383913.wav", "MinVoltage ": "+3.54"},
            "Zone 4 ": {"Sample ": "11L-The_Bobolink-1742491322488.wav", "MinVoltage ": "+3.00"},
            "Zone 5 ": {"Sample ": "11L-tube_bells-1742491266689.wav", "Side ": 1, "MinVoltage ": "+2.50"},
            "Zone 6 ": {"Sample ": "11L-sine_wave-1742491298615.wav", "MinVoltage ": "+1.99"},
            "Zone 7 ": {"Sample ": "11L-soft_female_speech_a-1742491275400.wav", "Side ": 1, "MinVoltage ": "+1.43"},
            "Zone 8 ": {"Sample ": "11L-tube_bells-1742491266689.wav", "Side ": 1, "MinVoltage ": "-5.00"}
        },
        "Channel 8 ": {
            "PlayMode ": 1,
            "LinFM ": "2A 1.00",
            "PitchCV ": "2B 0.50",
            "PMIndexMod ": "2A 1.00",
            "PanMod ": "2C 1.00",
            "XfadeGroup ": "A",
            "ZonesCV ": "1C",
            "Zone 1 ": {"Sample ": "11L-Air_raid_siren_dista-1742491271673.wav", "MinVoltage ": "+4.52"},
            "Zone 2 ": {"Sample ": "11L-cd_skipping_stereo_g-1742491458253.wav", "MinVoltage ": "+4.00"},
            "Zone 3 ": {"Sample ": "11L-electromagnetic_micr-1742491383913.wav", "MinVoltage ": "+3.54"},
            "Zone 4 ": {"Sample ": "11L-The_Bobolink-1742491322488.wav", "MinVoltage ": "+3.00"},
            "Zone 5 ": {"Sample ": "11L-tube_bells-1742491266689.wav", "Side ": 1, "MinVoltage ": "+2.50"},
            "Zone 6 ": {"Sample ": "11L-sine_wave-1742491298615.wav", "MinVoltage ": "+1.99"},
            "Zone 7 ": {"Sample ": "11L-soft_female_speech_a-1742491275400.wav", "Side ": 1, "MinVoltage ": "+1.43"},
            "Zone 8 ": {"Sample ": "11L-tube_bells-1742491266689.wav", "Side ": 1, "MinVoltage ": "-5.00"}
        }
    }
}

# Generate presets using the sample banks
for preset_num in range(1, NUM_PRESETS + 1):
    preset_key = f"Preset {preset_num} "
    preset_data = {preset_key: preset_template["Preset 15 "].copy()}
    preset_data[preset_key]["Name "] = f"Pre{preset_num}"

    # Assign unique bank of 8 samples to each channel
    preset_banks = sample_banks[preset_num - 1]

    for i in range(CHANNELS_PER_PRESET):
        channel_key = f"Channel {i + 1} "
        channel_samples = preset_banks[i]
        for j in range(SAMPLES_PER_CHANNEL):
            zone_key = f"Zone {j + 1} "
            preset_data[preset_key][channel_key][zone_key]["Sample "] = channel_samples[j]

    # Save with prstXXX.yml naming convention
    output_file = os.path.join(OUTPUT_DIR, f"prst{preset_num:03d}.yml")
    with open(output_file, "w") as f:
        yaml.dump(preset_data, f, Dumper=NoQuotesDumper, default_flow_style=False, sort_keys=False)

    print(f"Preset {preset_num} saved to {output_file}")

print("Preset generation complete!")