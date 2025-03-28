import os
import random
import yaml
import wave
from collections import defaultdict
import copy

# Directory containing samples
SAMPLES_DIR = "/Users/mikesidnam/Desktop/Keepers/NormalizedKeepers"
OUTPUT_DIR = "/Users/mikesidnam/Desktop/EditedKeepers"
NUM_PRESETS = 10
TEMPLATE_FILE = "/Users/mikesidnam/PycharmProjects/pythonProject5/prst001.yml"  # Path to your template YAML file

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Scan the directory for sample files and group by length
all_samples = [f for f in os.listdir(SAMPLES_DIR) if f.endswith(".wav")]
if len(all_samples) < 64:  # 8 channels * 8 zones = 64 samples minimum
    print("Warning: Fewer than 64 samples available. Duplicates may occur.")

# Group samples by length (optional, for same-length preference)
sample_groups = defaultdict(list)
for sample in all_samples:
    sample_path = os.path.join(SAMPLES_DIR, sample)
    try:
        with wave.open(sample_path, 'rb') as wav_file:
            length = wav_file.getnframes()
            sample_groups[length].append(sample)
    except wave.Error:
        print(f"Error reading {sample}. Skipping.")


# Custom YAML dumper to remove quotes from all strings
class NoQuotesDumper(yaml.SafeDumper):
    def represent_str(self, data):
        return self.represent_scalar('tag:yaml.org,2002:str', data, style='')


NoQuotesDumper.add_representer(str, NoQuotesDumper.represent_str)


# Load the preset template from a YAML file
def load_template(template_path):
    try:
        with open(template_path, 'r') as f:
            template = yaml.safe_load(f)
        # Assuming the template has a single top-level preset key (e.g., "Preset 15 ")
        preset_key = list(template.keys())[0]  # Get the first (and only) preset key
        return preset_key, template[preset_key]
    except FileNotFoundError:
        print(f"Error: Template file '{template_path}' not found.")
        raise
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error loading template: {e}")
        raise


# Load the template
template_key, preset_template = load_template(TEMPLATE_FILE)

# Generate presets
for preset_num in range(1, NUM_PRESETS + 1):
    # Deep copy the template and rename the preset key
    preset_key = f"Preset {preset_num} "
    preset_data = {preset_key: copy.deepcopy(preset_template)}  # Use deep copy to avoid modifying the template
    preset_data[preset_key]["Name"] = f"Pre{preset_num}"

    # Flatten sample groups into a single list if same-length grouping isn’t viable
    valid_groups = [group for length, group in sample_groups.items() if len(group) >= 8]
    if len(valid_groups) >= 8:
        # Use same-length groups if possible
        random.shuffle(valid_groups)
        selected_groups = valid_groups[:8]
    else:
        # Fall back to fully random selection
        selected_groups = [all_samples] * 8  # Use all samples for each channel

    # Assign random WAVs to each channel’s zones
    for i in range(8):
        channel_key = f"Channel {i + 1}"
        if channel_key not in preset_data[preset_key]:
            print(f"Warning: {channel_key} not found in template for preset {preset_num}. Skipping.")
            continue

        group_samples = selected_groups[i].copy()
        random.shuffle(group_samples)

        # Ensure we have enough samples, repeat if necessary
        while len(group_samples) < 8:
            group_samples.extend(group_samples[:8 - len(group_samples)])
        zones_samples = group_samples[:8]

        for j in range(8):
            zone_key = f"Zone {j + 1}"
            if zone_key not in preset_data[preset_key][channel_key]:
                print(f"Warning: {zone_key} not found in {channel_key} for preset {preset_num}. Skipping.")
                continue
            preset_data[preset_key][channel_key][zone_key]["Sample"] = zones_samples[j]

    # Save with prstXXX.yml naming convention
    output_file = os.path.join(OUTPUT_DIR, f"prst{preset_num:03d}.yml")
    with open(output_file, "w") as f:
        yaml.dump(preset_data, f, Dumper=NoQuotesDumper, default_flow_style=False, sort_keys=False)

    print(f"Preset {preset_num} saved to {output_file}")

print("Preset generation complete!")