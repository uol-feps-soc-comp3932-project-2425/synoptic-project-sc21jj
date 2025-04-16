import os
import shutil
import random
import argparse

def collect_files(directory):
    """Collect all .png files from a directory."""
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.png')]

def main():
    # Parse path to source directory and total number of samples as command line arguments
    parser = argparse.ArgumentParser(description="Randomly sample a given number of .png files from a specified directory.")
    parser.add_argument("source_dir", type=str, help="Path to the source directory")
    parser.add_argument("sample_size", type=int, help="Number of .png files to be sampled from source directory")
    args = parser.parse_args()
    
    # Randomly sample 'sample_size' .png files from source_dir
    files = collect_files(args.source_dir)
    num_samples = min(args.sample_size, len(files))
    sampled_files = random.sample(files, num_samples) if num_samples > 0 else []
    
    # Generate path to new downsample subdirectory (in the same parent directory as source_dir)
    parent_dir = os.path.dirname(args.source_dir)
    source_dir_name = os.path.basename(args.source_dir)
    downsample_dir = os.path.join(parent_dir, f"{source_dir_name}_downsample")
    os.makedirs(downsample_dir, exist_ok=True)
    
    # Copy all downsampled files into downsample subdirectory
    for file in sampled_files:
        shutil.copy(file, args.output_dir)
    
    print(f"Sampled {num_samples} files from {args.source_dir}.")
    print(f"Files copied to: {args.output_dir}")

if __name__ == "__main__":
    main()