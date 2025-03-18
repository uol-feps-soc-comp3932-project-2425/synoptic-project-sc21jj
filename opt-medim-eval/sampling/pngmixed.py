import os
import shutil
import random
import argparse

# Define the desired percentage split between real and synthetic samples
PERCENT_A = 95.0  # Change this value to adjust the percentage of real samples
PERCENT_B = 5.0   # Change this value to adjust the percentage of synthetic samples

def collect_files(directory):
    """Collect all .png files from a directory."""
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.png')]

def main():
    parser = argparse.ArgumentParser(description="Sample .png files from specified directories with percentage control.")
    parser.add_argument("dir_A", type=str, help="Path to real subdirectory")
    parser.add_argument("dir_B", type=str, help="Path to synthetic subdirectory")
    parser.add_argument("dir_C", type=str, help="Path to mixed subdirectory")
    args = parser.parse_args()
    
    # Define subdirectory name based on percentages
    subdir_name = f"{int(PERCENT_A)}-{int(PERCENT_B)}"
    output_dir = os.path.join(args.dir_C, subdir_name)
    os.makedirs(output_dir, exist_ok=True)
    
    # Collect .png files
    files_A = collect_files(args.dir_A)
    files_B = collect_files(args.dir_B)
    
    total_files = min(250, len(files_A) + len(files_B))
    
    if PERCENT_A + PERCENT_B != 100:
        print("Error: The sum of PERCENT_A and PERCENT_B must be 100.")
        return
    
    num_A = min(int((PERCENT_A / 100) * total_files), len(files_A))
    num_B = min(total_files - num_A, len(files_B))
    
    sampled_A = random.sample(files_A, num_A) if num_A > 0 else []
    sampled_B = random.sample(files_B, num_B) if num_B > 0 else []
    sampled_files = sampled_A + sampled_B
    
    # Shuffle final sample order
    random.shuffle(sampled_files)
    
    # Copy sampled files to the new subdirectory in dir_C
    for file in sampled_files:
        shutil.copy(file, output_dir)
    
    # Print results
    if total_files > 0:
        print(f"Sampled {num_A} files from dir_A and {num_B} files from dir_B.")
        print(f"Files copied to: {output_dir}")
    else:
        print("No .png files found in A or B.")

if __name__ == "__main__":
    main()