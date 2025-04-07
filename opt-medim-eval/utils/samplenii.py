import os
import gzip
import shutil
import random
import glob
import argparse

def find_nii_gz_files(root_dir):
    """Recursively finds all .nii.gz files under root_dir."""
    nii_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.nii.gz'):
                full_path = os.path.join(dirpath, filename)
                nii_files.append(full_path)
    return nii_files

def copy_sampled_files(files, destination, sample_size):
    """Randomly samples files and copies them to the destination directory."""
    sampled_files = random.sample(files, min(sample_size, len(files)))
    for file in sampled_files:
        shutil.copy(file, destination)
    return sampled_files

def decompress_nii_gz_files(directory):
    """Decompresses all .nii.gz files in the given directory."""
    for file in glob.glob(os.path.join(directory, "*.nii.gz")):
        output_file = file[:-3]  # Remove .gz extension
        with gzip.open(file, 'rb') as f_in, open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        os.remove(file)  # Remove the compressed file

def main():
    parser = argparse.ArgumentParser(description="Randomly sample 50 .nii files from an MRI imaging dataset")
    parser.add_argument("--source_dir", type=str, help="Path to the root directory containing all .nii files to sample from")
    parser.add_argument("--output_dir", type=str, help="Path to where the directory containing the sampled subset should be output")
    parser.add_argument("--sample_size", type=int, default=50, help="Number of .nii files to be sampled from source directory")
    args = parser.parse_args()

    # Step 1: Find all .nii.gz files in source directory
    all_nii_files = find_nii_gz_files(args.source_dir)

    # Step 2: Sample 'sample_size' files and copy them to root directory
    sampled_files = copy_sampled_files(all_nii_files, args.output_dir, args.sample_size)

    # Step 3: Decompress the copied files
    decompress_nii_gz_files(args.output_dir)

    print(f"Sampled {args.sample_size} .nii files from {args.source_dir}.")
    print(f"Files copied to: {args.output_dir}")

if __name__ == "__main__":
    main()