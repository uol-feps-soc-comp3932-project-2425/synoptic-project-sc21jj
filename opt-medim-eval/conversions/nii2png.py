import os
import sys
import numpy as np
import nibabel as nib
from PIL import Image

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
    """Convert all .nii files in the 'Real' directory to PNG format."""
    real_dir = os.path.join(root_dir, "Real")
    real_png_dir = os.path.join(root_dir, "realpng")

    if os.path.exists(real_dir):
        for file in os.listdir(real_dir):
            if file.endswith(".nii"):
                nii_path = os.path.join(real_dir, file)
                convert_nii_to_png(nii_path, real_png_dir)
                print(f"Converted {nii_path} -> {real_png_dir}")

def process_synthetic_directory(root_dir):
    """Convert all '.nii' files in 'Synthetic' to PNG format."""
    synthetic_dir = os.path.join(root_dir, "Synthetic")
    synthetic_png_dir = os.path.join(root_dir, "syntheticpng")

    if os.path.exists(synthetic_dir):
        for file in os.listdir(synthetic_dir):
            if file.endswith(".nii"):
                nii_path = os.path.join(synthetic_dir, file)
                convert_nii_to_png(nii_path, synthetic_png_dir)
                print(f"Converted {nii_path} -> {synthetic_png_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python nii2png.py <root_directory>")
        sys.exit(1)

    root_directory = sys.argv[1]

    # Process both 'Real' and 'Synthetic' directories
    process_real_directory(root_directory)
    process_synthetic_directory(root_directory)

    print("Conversion complete.")