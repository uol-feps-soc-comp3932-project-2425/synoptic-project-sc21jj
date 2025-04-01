import os
import shutil
import random
import argparse

def collect_files(directory):
    """Collect all .png files from a directory."""
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.png')]

def main():
    parser = argparse.ArgumentParser(description="Randomly sample 250 .png files from a specified directory.")
    parser.add_argument("source_dir", type=str, help="Path to the source directory")
    parser.add_argument("output_dir", type=str, help="Path to the output directory")
    args = parser.parse_args()
    
    files = collect_files(args.source_dir)
    num_samples = min(250, len(files))
    sampled_files = random.sample(files, num_samples) if num_samples > 0 else []
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    for file in sampled_files:
        shutil.copy(file, args.output_dir)
    
    print(f"Sampled {num_samples} files from {args.source_dir}.")
    print(f"Files copied to: {args.output_dir}")

if __name__ == "__main__":
    main()