# Generative Healthcare Applications: Investigating the Evaluation of Synthetic Medical Imaging to Improve Segmentation Performance

This is the online code repository for sc21jj's final submission for 24/25 COMP3932 Synoptic Project (EPA).

## Set-Up & Usage

### Set-Up

Clone the repository and install all required packages in a conda environment:

```
git clone git@github.com:uol-feps-soc-comp3932-project-2425/synoptic-project-sc21jj.git
cd synoptic-project-sc21jj
conda env create -f environment.yml
```

### Usage

Usage commands for all scripts in the repository are included below.

First, navigate to the opt-medim-eval directory:

```bash
cd opt-medim-eval
```

#### Cross-compare

For cross-comparison scripts, navigate to the crosscompare subdirectory:

```bash
cd crosscompare
```

cleardirectories.py, a script for keeping files clearing redundant subdirectories, can be run using the following command:

```bash
python cleardirectories.py 
```

#### Evaluation

For evaluation scripts, navigate to the evaluation subdirectory:

```bash
cd evaluation 
```

eval_findings.py, a script for calculating relevant statistics and plotting graphs based on dgm-eval result statistics, can be run using the following command:

```bash
python eval_findings.py [name_of_dataset] [name_of_encoder] --findings [type_of_finding]
```

frechetcoefficient.py, a script for calculating Frechet coefficient scores for a given dataset category, can be run using the following command:

```bash
python frechetcoefficient.py [dataset_category]
```

#### Sampling

For sampling scripts, navigate to the sampling subdirectory:

```bash
cd sampling
```

pngmixedsubset.py, a script for generating a mixed random sample of MRI .png files, can be run using the following command:

```bash
python pngmixedsubset.py 
```

pngrandomsubset.py, a script for randomly sampling MRI .png files, can be run using the following command:

```bash
python pngrandomsubset.py
```

sliceperscan.py, a script for randomly sampling a single MRI slice .png file, can be run using the following command:

```bash
python sliceperscan.py
```

traintestsplit.py, a script for generating training and test subsets, can be run using the following command:

```bash
python traintestsplit.py [source_directory]
```

#### Segmentation

For segmentation scripts, navigate to the segmentation subdirectory:

```bash
cd segmentation
```

evanyseg_sampling.py, a script for sampling medical image .png files to prepare for running EvanySeg, can be run using the following command:

```bash
python evanyseg_sampling.py [num_to_sample] [real_percentage] [synthetic_percentage] [output_directory] --trn [training_percentage] 
```

evanyseg_resultstats.py, a script for calculating relevant statistics on the output of EvanySeg, can be run using the following command:

```bash
python evanyseg_resultstats.py [path_to_evanyseg_result_csv_file]
```

seg_findings.py, a script for calculating relevant statistics and plotting graphs based on EvanySeg result statistics, can be run using the following command:

```bash
python seg_findings.py [name_of_dataset] --findings [type_of_finding]
```

#### Utils

For utils scripts, navigate to the utils subdirectory:

```bash
cd utils
```

cleardirectories.py, a script for keeping relevant files and clearing redundant subdirectories, can be run using the following command:

```bash
python cleardirectories.py 
```

collapsenii.py, a script for extracting NiFTi files from complex subdirectories, can be run using the following command:

```bash
python collapsenii.py 
```

nii2png.py, a script for converting NiFTi files to .png format, can be run using the following command:

```bash
python nii2png.py [real_directory] [synthetic_directory]
```

pngclean.py, a script for deleting redundant MRI .png slices, can be run using the following command:

```bash
python pngclean.py [source_directory] [slice_num_to_delete]
```

samplenii.py, a script for sampling NiFTi files, can be run using the following command:

```bash
python samplenii.py [source_directory] [output_directory] --sample_size [size_of_sample]
```

## Acknowledgements

I thank the associated researchers for providing publicly available source code for the following codebases used as part of this project's research and implemention:
- [dgm-eval](https://github.com/layer6ai-labs/dgm-eval): used for synthetic image evaluation
- [frechet-coefficient](https://github.com/adriankucharski/frechet-coefficient) : used for synthetic image evaluation
- [MedSAM](https://github.com/bowang-lab/MedSAM) : used for segmentation mask generation
- [EvanySeg](https://github.com/ahjolsenbics/EvanySeg) : used for segmentation evaluation
