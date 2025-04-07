import os
import sys
import numpy as np
import nibabel as nib
from PIL import Image
import argparse

def nii2png(nii_path, png_dir):
    """Convert a .nii file to PNG images and save them in the specified directory."""
    os.makedirs(png_dir, exist_ok=True)  # Ensure target directory exists

    # Load .nii file
    img = nib.load(nii_path)
    data = img.get_fdata()

    # Remove singleton dimensions
    data = np.squeeze(data)

    # Normalize data to 8-bit grayscale
    data_min, data_max = np.min(data), np.max(data)
    if data_max > data_min:
        data = (data - data_min) / (data_max - data_min) * 255.0
    data = data.astype(np.uint8)

    base_name = os.path.splitext(os.path.basename(nii_path))[0]

    if data.ndim == 3:
        # Save each slice for 3D data
        for i in range(data.shape[2]):
            slice_img = data[:, :, i]
            img_pil = Image.fromarray(slice_img)
            img_pil.save(os.path.join(png_dir, f"{base_name}_slice_{i}.png"))

    elif data.ndim == 4:
        # Save each time frame and slice for 4D data
        for t in range(data.shape[3]):
            for i in range(data.shape[2]):
                slice_img = data[:, :, i, t]
                img_pil = Image.fromarray(slice_img)
                img_pil.save(os.path.join(png_dir, f"{base_name}_time_{t}_slice_{i}.png"))

def process_real_directory(root_dir):
    """Convert all real .nii files to PNG format."""
    real_nii_dir = root_dir
    real_parent_dir = os.path.dirname(real_nii_dir)
    real_png_dir = os.path.join(real_parent_dir, "realpng")

    if os.path.exists(real_nii_dir):
        for file in os.listdir(real_nii_dir):
            if file.endswith(".nii"):
                nii_path = os.path.join(real_nii_dir, file)
                nii2png(nii_path, real_png_dir)
                print(f"Converted {nii_path} -> {real_png_dir}")

def process_synthetic_directory(root_dir):
    """Convert all synthetic .nii files to PNG format."""
    synth_nii_dir = root_dir
    synth_parent_dir = os.path.dirname(synth_nii_dir)
    synth_png_dir = os.path.join(synth_parent_dir, "synthpng")

    if os.path.exists(synth_nii_dir):
        for file in os.listdir(synth_nii_dir):
            if file.endswith(".nii"):
                nii_path = os.path.join(synth_nii_dir, file)
                nii2png(nii_path, synth_png_dir)
                print(f"Converted {nii_path} -> {synth_png_dir}")

def main():
    parser = argparse.ArgumentParser(description="Randomly sample 50 .nii files from an MRI imaging dataset")
    parser.add_argument("--real_dir", type=str, help="Path to the directory containing the real .nii files")
    parser.add_argument("--synth_dir", type=str, help="Path to the directory containing the real .nii files")
    args = parser.parse_args()

    # Process both 'Real' and 'Synthetic' directories
    #process_real_directory(args.real_dir)
    process_synthetic_directory(args.synth_dir)

    print("Conversion complete.")

if __name__ == "__main__":
    main()