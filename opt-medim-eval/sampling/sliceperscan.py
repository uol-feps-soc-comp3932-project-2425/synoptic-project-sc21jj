import os
import random
import sys
import shutil

def sample_real_slices(source_dir, target_dir):
    """Randomly selects one .png slice per scan across all timestamps and saves it."""
    if not os.path.exists(source_dir):
        print(f"Directory not found: {source_dir}")
        return

    os.makedirs(target_dir, exist_ok=True)  # Ensure target directory exists

    scan_dict = {}

    # Group PNG files based on their original scan name (ignoring timestamps)
    for file in os.listdir(source_dir):
        if file.endswith(".png"):
            parts = file.split("_")
            if "time" in parts:
                scan_name = "_".join(parts[:-4])  # Ignore timestamps and slice number
            else:
                scan_name = "_".join(parts[:-2])  # Standard non-timestamped files
            
            if scan_name not in scan_dict:
                scan_dict[scan_name] = []
            scan_dict[scan_name].append(file)

    # Randomly select one slice per scan and copy it to the target directory
    for scan_name, slices in scan_dict.items():
        chosen_slice = random.choice(slices)  # Select one at random
        src_path = os.path.join(source_dir, chosen_slice)
        dest_path = os.path.join(target_dir, chosen_slice)
        shutil.copy(src_path, dest_path)  # Copy instead of delete
        print(f"Copied: {chosen_slice} -> {target_dir}")

def sample_synthetic_slices(source_dir, target_dir):
    """Randomly selects one .png slice per scan in the synthetic directory."""
    if not os.path.exists(source_dir):
        print(f"Directory not found: {source_dir}")
        return

    os.makedirs(target_dir, exist_ok=True)  # Ensure target directory exists

    scan_dict = {}

    # Group PNG files based on their original scan name
    for file in os.listdir(source_dir):
        if file.endswith(".png"):
            scan_name = "_".join(file.split("_")[:-2])  # Remove slice number info
            if scan_name not in scan_dict:
                scan_dict[scan_name] = []
            scan_dict[scan_name].append(file)

    # Randomly select one slice per scan and copy it to the target directory
    for scan_name, slices in scan_dict.items():
        chosen_slice = random.choice(slices)  # Select one at random
        src_path = os.path.join(source_dir, chosen_slice)
        dest_path = os.path.join(target_dir, chosen_slice)
        shutil.copy(src_path, dest_path)  # Copy instead of delete
        print(f"Copied: {chosen_slice} -> {target_dir}")

def process_directories(root_dir):
    """Processes realpng and syntheticpng directories and outputs sampled images."""
    real_png_dir = os.path.join(root_dir, "realpng")
    synthetic_png_dir = os.path.join(root_dir, "syntheticpng")

    sampled_real_png_dir = os.path.join(root_dir, "sampled_realpng")
    sampled_synthetic_png_dir = os.path.join(root_dir, "sampled_syntheticpng")

    sample_real_slices(real_png_dir, sampled_real_png_dir)
    sample_synthetic_slices(synthetic_png_dir, sampled_synthetic_png_dir)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sample_slices.py <root_directory>")
        sys.exit(1)

    root_directory = sys.argv[1]
    process_directories(root_directory)

    print("Sampling complete.")