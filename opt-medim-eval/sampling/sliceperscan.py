import os
import shutil
import random
import re
import argparse

def sample_slices(source_dir, target_dir):
    """
    Randomly selects one .png slice per scan (grouped by the prefix before '_slice_') 
    and saves it to the target directory.
    """
    if not os.path.exists(source_dir):
        print(f"Directory not found: {source_dir}")
        return

    os.makedirs(target_dir, exist_ok=True)

    pattern = re.compile(r'^(.*)_slice_(\d+)\.png$')
    scan_dict = {}

    for file in os.listdir(source_dir):
        if file.endswith(".png"):
            match = pattern.match(file)
            if match:
                scan_name = match.group(1)
                if scan_name not in scan_dict:
                    scan_dict[scan_name] = []
                scan_dict[scan_name].append(file)

    for scan_name, slices in scan_dict.items():
        chosen_slice = random.choice(slices)
        src_path = os.path.join(source_dir, chosen_slice)
        dest_path = os.path.join(target_dir, chosen_slice)
        shutil.copy(src_path, dest_path)
        print(f"Copied: {chosen_slice} -> {target_dir}")

def process_directories(real_dir, synth_dir):
    """Processes realpng and syntheticpng directories and outputs downsampled slices."""
    real_png_dir = os.path.join(real_dir, "realpng")
    synth_png_dir = os.path.join(synth_dir, "synthpng")

    #sampled_real_png_dir = os.path.join(real_dir, "sampled_realpng")
    sampled_synthetic_png_dir = os.path.join(synth_dir, "sampled_syntheticpng")
    #os.makedirs(sampled_real_png_dir, exist_ok=True)
    os.makedirs(sampled_synthetic_png_dir, exist_ok=True)

    #sample_slices(real_png_dir, sampled_real_png_dir)
    sample_slices(synth_png_dir, sampled_synthetic_png_dir)

def main():
    parser = argparse.ArgumentParser(description="Randomly downsample MRI slice .png files from a specified directory to keep only one slice per scan.")
    parser.add_argument("real_directory", type=str, help="Path to the real MRI source directory")
    parser.add_argument("synthetic_directory", type=str, help="Path to the synthetic MRI source directory")
    args = parser.parse_args()

    process_directories(args.real_directory, args.synthetic_directory)

    print("Slice downsampling complete.")

if __name__ == "__main__":
    main()
