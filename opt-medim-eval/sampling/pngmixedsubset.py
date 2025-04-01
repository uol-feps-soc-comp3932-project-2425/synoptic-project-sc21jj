import os
import shutil
import argparse

def collect_files(directory):
    """Collect all .png files from a directory in original order."""
    return sorted([os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.png')])

def main():
    parser = argparse.ArgumentParser(description="Sample .png files from specified directories with percentage control.")
    parser.add_argument("real_dir", type=str, help="Path to real subdirectory")
    parser.add_argument("synth_dir", type=str, help="Path to synthetic subdirectory")
    parser.add_argument("mixed_dir", type=str, help="Path to mixed subdirectory")
    parser.add_argument("percentage_real", type=float, help="Percentage of real images (e.g., 0.9 for 90%)")
    parser.add_argument("total_samples", type=int, help="Total number of images to be sampled")
    args = parser.parse_args()
    
    if not (0 <= args.percentage_real <= 1):
        print("Error: percentage_real must be between 0 and 1.")
        return
    
    real_files = collect_files(args.real_dir)
    synth_files = collect_files(args.synth_dir)
    
    total_files_available = len(real_files) + len(synth_files)
    total_samples = min(args.total_samples, total_files_available)
    
    num_real = min(int(args.percentage_real * total_samples), len(real_files))
    num_synth = total_samples - num_real
    
    sampled_real = real_files[:num_real] if num_real > 0 else []
    sampled_synth = synth_files[:num_synth] if num_synth > 0 else []
    sampled_files = sampled_real + sampled_synth
    
    # Define subdirectory name based on percentages
    subdir_name = f"{int(args.percentage_real * 100)}-{int((1 - args.percentage_real) * 100)}"
    output_dir = os.path.join(args.mixed_dir, subdir_name)
    os.makedirs(output_dir, exist_ok=True)
    
    # Copy sampled files to the new subdirectory in mixed_dir
    for file in sampled_files:
        shutil.copy(file, output_dir)
    
    print(f"Sampled {num_real} files from real_dir and {num_synth} files from synth_dir.")
    print(f"Files copied to: {output_dir}")

if __name__ == "__main__":
    main()