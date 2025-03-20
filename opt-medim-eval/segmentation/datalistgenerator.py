import os
import json
import random
import shutil
import tempfile
import argparse
import yaml

def generate_datalist(dscategory, realpct, dataroot):

    test_dir = os.path.join(dataroot, "Test/")
    train_dir = os.path.join(dataroot, "Training/")
    label_dir = os.path.join(dataroot, "Labels/")

    datalist_json = {"testing": [], "training": []}

    # Populate JSON with testing images
    datalist_json["testing"] = [
        {"image": "./Test/" + file} for file in os.listdir(test_dir) if (".nii" in file) and ("._" not in file)
    ]

    # Populate JSON with training images and labels
    datalist_json["training"] = [
        {"image": "./Training/" + file, "label": "./Labels/" + file, "fold": 0}
        for file in os.listdir(train_dir)
        if (".nii" in file) and ("._" not in file)
    ]  # Initialize as single fold

    datalist_json["training"][:10]

    # Randomise training data
    random.seed(42)
    random.shuffle(datalist_json["training"])

    # Split training data into N random folds
    num_folds = 5
    fold_size = len(datalist_json["training"]) // num_folds
    for i in range(num_folds):
        for j in range(fold_size):
            datalist_json["training"][i * fold_size + j]["fold"] = i

    # Format datalist file name
    synthpct = 100 - realpct
    datalist_file = f"{dscategory}{realpct}-{synthpct}.json"

    # Obtain and construct filepath for datalist
    root_dir = os.path.dirname(os.path.abspath(__file__))
    datalist_filepath = f"{root_dir}/datalists/{datalist_file}"

    # Save JSON to file
    with open(datalist_filepath, "w", encoding="utf-8") as f:
        json.dump(datalist_json, f, ensure_ascii=False, indent=4)
    print(f"Datalist is saved to {datalist_filepath}")

    # Return datalist filename for task file generation
    return datalist_file

def generate_taskfile(dscategory, realpct, dataroot, dlfilename):

    task_yaml = {
        "modality": None,
        "datalist": None,
        "dataroot": None
    }

    if 'mri' in dscategory:
        task_yaml["modality"] = "MRI"
    elif 'ct' in dscategory:
        task_yaml["modality"] = "CT"

    task_yaml["datalist"] = f"./datalists/{dlfilename}"

    task_yaml["dataroot"] = f"./{dataroot}"

    # Format task file name
    synthpct = 100 - realpct
    task_file = f"{dscategory}{realpct}-{synthpct}.yaml"

    # Obtain and construct filepath for task file
    root_dir = os.path.dirname(os.path.abspath(__file__))
    task_filepath = f"{root_dir}/taskfiles/{task_file}"
    
    with open(task_filepath, "w") as f:
        yaml.dump(task_yaml, f, default_flow_style=False, sort_keys=False, default_style="")

    with open(task_filepath, "r") as f:
        lines = f.readlines()
    
    with open(task_filepath, "w") as f:
        for line in lines:
            if "datalist:" in line or "dataroot:" in line:
                line = line.replace(" ", " \"").rstrip() + "\"\n"
            f.write(line)
    
    print(f"Task file is saved to {task_filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate formatted datalist for Auto3DSeg AutoRunner")
    parser.add_argument("--ds_category", type=str, required=True, help="Dataset category being sampled from [ganmri/ganct/dmmri/dmct]")
    parser.add_argument("--percent_real", type=int, required=True, help="Percentage of real imaging data in mixed dataset")
    parser.add_argument("--root_dir", type=str, required=True, help="Directory containing the test and training subdirectories")
    args = parser.parse_args()
    
    datalist = generate_datalist(args.ds_category, args.percent_real, args.root_dir)
    generate_taskfile(args.ds_category, args.percent_real, args.root_dir, datalist)