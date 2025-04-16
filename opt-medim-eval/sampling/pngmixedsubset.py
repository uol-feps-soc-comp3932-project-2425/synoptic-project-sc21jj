import os
import shutil
import argparse

def collect_files(directory):
    """Collect all .png files from a directory in original order."""
    return sorted([os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.png')])

def gen_mixed_subset(realdir, synthdir, mixeddir, realpct, n):
    """Generate a mixed subset of real and synthetic files and copy them into a new directory."""

    # Validate percentage input
    if not (0 <= realpct <= 1):
        print("Error: percentage_real must be between 0 and 1.")
        return
    
    # Collect file paths from both real and synthetic directories
    real_files = collect_files(realdir)
    synth_files = collect_files(synthdir)
    
    # Determine how many total files can be sampled
    total_files_available = len(real_files) + len(synth_files)
    total_samples = min(n, total_files_available)
    
    # Calculate number of files to sample from each category
    num_real = min(int(realpct * total_samples), len(real_files))
    num_synth = total_samples - num_real
    
    # Sample the files (use first N files as a simple sampling strategy)
    sampled_real = real_files[:num_real] if num_real > 0 else []
    sampled_synth = synth_files[:num_synth] if num_synth > 0 else []
    sampled_files = sampled_real + sampled_synth
    
    # Create output subdirectory based on the real/synthetic ratio
    subdir_name = f"{int(realpct * 100)}-{int((1 - realpct) * 100)}"
    output_dir = os.path.join(mixeddir, subdir_name)
    os.makedirs(output_dir, exist_ok=True)
    
    # Copy sampled files to the new subdirectory in mixed_dir
    for file in sampled_files:
        shutil.copy(file, output_dir)
    
    print(f"Sampled {num_real} files from real_dir and {num_synth} files from synth_dir.")
    print(f"Files copied to: {output_dir}")

def main():
    # Parse paths to real and synthetic PNG directories, path to output directory, percentage of real images in mixed data and total number of samples as command line arguments
    parser = argparse.ArgumentParser(description="Generate a mixed sample for real and synthetic MRI .png files with percentage control")
    parser.add_argument("real_dir", type=str, help="Path to real subdirectory")
    parser.add_argument("synth_dir", type=str, help="Path to synthetic subdirectory")
    parser.add_argument("mixed_dir", type=str, help="Path to mixed subdirectory")
    parser.add_argument("percentage_real", type=float, help="Percentage of real images (e.g., 0.9 for 90%)")
    parser.add_argument("total_samples", type=int, help="Total number of images to be sampled")
    args = parser.parse_args()
    
    gen_mixed_subset(args.real_dir, args.synth_dir, args.mixed_dir, args.percentage_real, args.total_samples)

if __name__ == "__main__":
    main()