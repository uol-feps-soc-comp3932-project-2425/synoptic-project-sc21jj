import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse

standard_synth_pcts = [0, 50, 60, 70, 80, 90, 100] # Initialising default synthetic percentage values

# Initialising GANMRI data dictionaries

ganmri_inception_data = {
    'Synthetic Percentage': standard_synth_pcts,
    'FD': [0.0000654, 97.71195507, 118.8942583, 142.5396132, 163.8193511, 187.5085843, 209.3618621],
    'Precision': [1, 0.62, 0.56, 0.47, 0.4, 0.33, 0.25],
    'Recall': [1, 0.9, 0.89, 0.82, 0.76, 0.69, 0.18],
    'Unbiased FD': [2.013471763, 102.0835921, 113.860521, 131.9922264, 162.933675, 185.2450433, 208.9602984],
    'FC': [1.00000022, 0.747001173, 0.703054373, 0.651567962, 0.608663737, 0.561420789, 0.525153788],
    'Density': [1.004, 0.56, 0.482, 0.368, 0.284, 0.182, 0.092],
    'Coverage': [1, 0.96, 0.93, 0.76, 0.67, 0.49, 0.21]
}

ganmri_dinov2_data = {
    'Synthetic Percentage': standard_synth_pcts,
    'FD': [0.000229, 283.5476695, 366.6268334, 445.2439924, 533.3296646, 603.146376, 692.9561115],
    'Precision': [1, 0.71, 0.66, 0.61, 0.55, 0.49, 0.43],
    'Recall': [1, 0.92, 0.92, 0.88, 0.87, 0.8, 0.31],
    'Unbiased FD': [6.644958616, 298.9368115, 339.1634104, 386.7411878, 504.3291383, 546.2169838, 696.5212567],
    'FC': [1.000000071, 0.802613355, 0.768349421, 0.726165703, 0.679205328, 0.628505494, 0.523221794],
    'Density': [1, 0.584, 0.48, 0.418, 0.35, 0.218, 0.158],
    'Coverage': [1, 0.98, 0.9, 0.77, 0.69, 0.38, 0.2]
}

ganmri_swav_data = {
    'Synthetic Percentage': [0, None, None, None, 80, 90, 100],
    'FD': [-0.00000260227, None, None, None, 1.72551823829725, 1.07266644193531, -0.00000260227],
    'Precision': [1, None, None, None, 0.8125, 0.9125, 1],
    'Recall': [1, None, None, None, 0.975, 0.975, 1],
    'Unbiased FD': [-0.026181584, None, None, None, 1.699023911, 1.16420987, 0.059362462],
    'Density': [1, None, None, None, 0.785, 0.91, 1],
    'Coverage': [1, None, None, None, 1, 1, 1]
}

ganmri_all_data = {
    "Inception": ganmri_inception_data,
    "DINOv2": ganmri_dinov2_data,
    "SwAV": ganmri_swav_data
}

# Initialising DMMRI data dictionaries

dmmri_inception_data = {
    'Synthetic Percentage': standard_synth_pcts,
    'FD': [-0.000152408, 83.53286168, 100.3606771, 114.4805349, 138.1902068, 155.750424, 175.3303901],
    'Precision': [0.9, 0.65, 0.6125, 0.575, 0.5125, 0.4125, 0.45],
    'Recall': [0.9, 0.95, 0.875, 0.85, 0.85, 0.6375, 0.375],
    'Unbiased FD': [-5.794803697, 82.01276525, 97.61067271, 113.9103102, 137.3491422, 153.5731494, 170.7922797],
    'FC': [1.000000421, 0.783679559, 0.742143555, 0.703281124, 0.662785039, 0.618545626, 0.552490349],
    'Density': [0.8825, 0.51, 0.415, 0.3875, 0.285, 0.2275, 0.2425],
    'Coverage': [0.9, 0.825, 0.6875, 0.6625, 0.55, 0.4, 0.325]
}

dmmri_dinov2_data = {
    'Synthetic Percentage': standard_synth_pcts,
    'FD': [-0.001080752, 720.8734354, 876.7355498, 960.6384922, 1171.32925, 1351.299725, 1595.893447],
    'Precision': [0.9, 0.6875, 0.65, 0.6375, 0.625, 0.5625, 0.55],
    'Recall': [0.9, 0.975, 0.8875, 0.8875, 0.9125, 0.7375, 0.2375],
    'Unbiased FD': [-66.66081855, 701.6441843, 811.5327192, 914.6295131, 1111.290756, 1382.193431, 1561.709643],
    'FC': [1.000000161, 0.838096779, 0.804877489, 0.771862341, 0.733399949, 0.671590925, 0.477439825],
    'Density': [0.88, 0.505, 0.4125, 0.3875, 0.325, 0.2475, 0.2175],
    'Coverage': [0.9, 0.825, 0.675, 0.625, 0.55, 0.3625, 0.15]
}

dmmri_all_data = {
    "Inception": dmmri_inception_data,
    "DINOv2": dmmri_dinov2_data,    
}

def normalise_metric(series, min_val=None, max_val=None, higher_is_better=True):
    """
    Normalise a metric using min-max scaling.
    Ignores None values in the series.
    Optionally inverts scale if higher_is_better is False.
    """
    series = pd.Series(series, dtype='float')

    # Drop None/NaN values for normalisation
    valid_series = series.dropna()

    # Use percentiles if no explicit min/max are provided
    if min_val is None:
        min_val = np.percentile(valid_series, 1)
    if max_val is None:
        max_val = np.percentile(valid_series, 99)

    # Handle edge case: constant metric values
    if max_val == min_val:
        norm_values = [1.0 if higher_is_better else 0.0] * len(valid_series)
    else:
        # Apply min-max normalisation
        norm = (valid_series - min_val) / (max_val - min_val)
        norm = np.clip(norm, 0, 1) # Clip values to [0, 1] range
        if higher_is_better == False:
            norm = 1 - norm # Invert if lower values are better
        norm_values = norm.tolist()

    # Reconstruct full list with None in original positions
    result = []
    norm_iter = iter(norm_values)
    for val in series:
        result.append(next(norm_iter) if pd.notna(val) else None)

    return result

def normalise_metric_values(data_dict_to_normalise, swav=False):
    """Normalise a dictionary of metric values using min-max normalisation."""
    if swav == True:
        # Normalise metrics specific to SwAV configuration
        normalised_dict = {
            'Synthetic Percentage': [0, 80, 90, 100], # Preset vakyes for SwAV
            'FD': normalise_metric(data_dict_to_normalise['FD'], higher_is_better=False),
            'Precision': normalise_metric(data_dict_to_normalise['Precision']),
            'Recall': normalise_metric(data_dict_to_normalise['Recall']),
            'Unbiased FD': normalise_metric(data_dict_to_normalise['Unbiased FD'], higher_is_better=False),
            'Density': normalise_metric(data_dict_to_normalise['Density']),
            'Coverage': normalise_metric(data_dict_to_normalise['Coverage']),
        }
        return normalised_dict
    else:
        # Normalise metrics using general configuration
        normalised_dict = {
            'Synthetic Percentage': standard_synth_pcts, # Use predefined percentages
            'FD': normalise_metric(data_dict_to_normalise['FD'], higher_is_better=False),
            'Precision': normalise_metric(data_dict_to_normalise['Precision']),
            'Recall': normalise_metric(data_dict_to_normalise['Recall']),
            'Unbiased FD': normalise_metric(data_dict_to_normalise['Unbiased FD'], higher_is_better=False),
            'FC': normalise_metric(data_dict_to_normalise['FC']),
            'Density': normalise_metric(data_dict_to_normalise['Density']),
            'Coverage': normalise_metric(data_dict_to_normalise['Coverage']),
        }
        return normalised_dict

def calc_correlation_coefficient(corrcoef_data_dict):
    """
    Compute correlation coefficients between the percentage of synthetic training data
    and up to seven user-provided variables:
        - 'Synthetic Percentage'
        - 'FD'
        - 'Precision'
        - 'Recall'
        - 'Unbiased FD'
        - 'FC'
        - 'Density'
        - 'Coverage'

    Parameters:
        data_dict (dict): Dictionary with the following keys:
        - 'Synthetic Percentage'
        - 'FD'
        - 'Precision'
        - 'Recall'
        - 'Unbiased FD'
        - 'FC'
        - 'Density'
        - 'Coverage'

    Returns:
        pd.Series: Correlation coefficients indexed by variable name.
    """

    # Convert dict to DataFrame
    data = pd.DataFrame(corrcoef_data_dict)

    # Variables to correlate
    variables = list(corrcoef_data_dict.keys())[1:]

    # Compute Pearson correlation with synthetic_percentage
    correlations = {
        var: np.corrcoef(data['Synthetic Percentage'], data[var])[0, 1] for var in variables
    }

    print(pd.Series(correlations, name='correlation_with_synthetic_percentage'))

def plot_metric_graph(metric, synth_pcts, i_vals, dino_vals, swav_vals=None, ax=None):
    # If an axis is provided, set matrix to true to indicate that the graph is being plotted as part of a matrix
    if ax != None:
        matrix = True

    # If no axis is provided, we create a new one (for individual use cases, but we expect ax in the main function)
    if ax is None:
        matrix = False
        fig, ax = plt.subplots(figsize=(10, 6))  # Create a new figure and axis if ax is None
    
    # Plot the first encoder's data
    ax.plot(synth_pcts, i_vals, label='Inception', marker='o', linestyle='-', color='blue')
    
    # Plot the second encoder's data if available
    ax.plot(synth_pcts, dino_vals, label='DINOv2', marker='x', linestyle='--', color='green')
    
    # Plot the third encoder's data if available
    if swav_vals is not None:
        ax.plot(synth_pcts, swav_vals, label='SwAV', marker='s', linestyle='-.', color='red')
    
    # Labels and title
    ax.set_xlabel('Synthetic Percentage')
    ax.set_ylabel(metric)
    ax.set_title(f"{metric} Value by Synthetic Training Data %")
    
    # Show a legend to label each encoder
    ax.legend()
    ax.grid(True)

    if matrix == False:
        plt.show()

def plot_metric_graphs(dataset, synth_pcts):
    # Define the metrics to plot
    metrics = ["FD", "Precision", "Recall", "Unbiased FD", "FC", "Density", "Coverage"]

    # Generate plots for each metric
    for metric in metrics:

        # Collect values for each encoder
        i_vals = dataset["Inception"][metric]
        dino_vals = dataset["DINOv2"][metric]
        swav_vals = None
        if "SwAV" in dataset.keys():
            if metric != 'FC':
                swav_vals = dataset["SwAV"][metric]

        # Plot using the custom function
        plot_metric_graph(metric, synth_pcts, i_vals, dino_vals, swav_vals)

def plot_normalised_metric_graphs(dataset, synth_pcts):
    # Define the metrics to plot
    metrics = ["FD", "Precision", "Recall", "Unbiased FD", "FC", "Density", "Coverage"]

    # Normalise dataset values
    for encoder in dataset.keys():
        if encoder == "SwAV":
            dataset[encoder] = normalise_metric_values(dict(list(dataset[encoder].items())[1:]), True)
        else:
            dataset[encoder] = normalise_metric_values(dict(list(dataset[encoder].items())[1:]))

    # Generate plots for each metric
    for metric in metrics:
        # Collect values for each encoder
        i_vals = dataset["Inception"][metric]
        dino_vals = dataset["DINOv2"][metric]
        swav_vals = None
        if "SwAV" in dataset.keys():
            if metric != 'FC':
                swav_vals = dataset["SwAV"][metric]

        # Plot using plot_metric_graph function
        plot_metric_graph(metric, synth_pcts, i_vals, dino_vals, swav_vals)

def generate_metric_graph_matrix(dataset, synth_pcts):
    # Define the metrics to plot
    metrics = ["FD", "Precision", "Recall", "Unbiased FD", "FC", "Density", "Coverage"]
    
    # Create a figure with a 2x4 grid (to accommodate 7 graphs, we use 2 rows and 4 columns)
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))  # Adjust the size as needed
    axes = axes.flatten()  # Flatten the 2x4 grid to easily access each axis

    # Normalise dataset values
    for encoder in dataset.keys():
        if encoder == "SwAV":
            dataset[encoder] = normalise_metric_values(dict(list(dataset[encoder].items())[1:]), True)
        else:
            dataset[encoder] = normalise_metric_values(dict(list(dataset[encoder].items())[1:]))

    # Generate plots for each metric and assign them to a subplot
    for i, metric in enumerate(metrics):
        # Collect values for each encoder
        i_vals = dataset["Inception"][metric]
        dino_vals = dataset["DINOv2"][metric]
        swav_vals = None
        if "SwAV" in dataset.keys():
            if metric != 'FC':
                swav_vals = dataset["SwAV"][metric]
        
        # Plot the graph on the correct subplot
        ax = axes[i]
        plot_metric_graph(metric, synth_pcts, i_vals, dino_vals, swav_vals, ax=ax)

    # Adjust layout for readability
    plt.tight_layout()
    plt.show()

def main():
    # Parse dataset category, encoder network and type of finding as command line arguments
    parser = argparse.ArgumentParser(description="Plot findings of evaluation metric experiments")
    parser.add_argument("--dataset", type=str, default=None, help="Name of the dataset that the experiments were conducted on (e.g. GANMRI, DMMRI)")
    parser.add_argument("--encoder", type=str, default=None, help="Name of the feature extractor encoder used for the experiments (e.g. inception, dinov2, swav)")
    parser.add_argument("--findings", type=str, default="all", help="Type of evaluation metric findings to plot (e.g. corrcoef, normalise, metricmatrix).")
    args = parser.parse_args()

    # Calculating findings for GANMRI data
    if args.dataset == "ganmri":
        # Calculate correlation coefficient values for each encoder
        if args.encoder == "inception":
            if args.findings == "corrcoef":
                calc_correlation_coefficient(ganmri_inception_data)
            if args.findings == "all":
                calc_correlation_coefficient(ganmri_inception_data)
        elif args.encoder == "dinov2":
            if args.findings == "corrcoef":
                calc_correlation_coefficient(ganmri_dinov2_data)
            if args.findings == "all":
                calc_correlation_coefficient(ganmri_dinov2_data)
        elif args.encoder == "swav":
            if args.findings == "corrcoef":
                calc_correlation_coefficient(ganmri_swav_data)
            if args.findings == "all":
                calc_correlation_coefficient(ganmri_swav_data)
        elif args.encoder == None:
            # Output normalised metric values for each GANMRI data dictionary
            if args.findings == "normalise":
                print(normalise_metric_values(dict(list(ganmri_inception_data.items())[1:])))
                print(normalise_metric_values(dict(list(ganmri_dinov2_data.items())[1:])))
                print(normalise_metric_values(dict(list(ganmri_swav_data.items())[1:]), True))
            # Output graphs for each GANMRI metric
            elif args.findings == "metrics":
                plot_metric_graphs(ganmri_all_data, standard_synth_pcts)
            # Output graphs for each GANMRI normalised metric
            elif args.findings == "normalisedmetrics":
                plot_normalised_metric_graphs(ganmri_all_data, standard_synth_pcts)
            # Output GANMRI metric graph matrix
            elif args.findings == "metricmatrix":
                generate_metric_graph_matrix(ganmri_all_data, standard_synth_pcts)
    # Calculating findings for GANMRI data
    if args.dataset == "dmmri":
        # Calculate correlation coefficient values for each encoder
        if args.encoder == "inception":
            if args.findings == "corrcoef":
                calc_correlation_coefficient(dmmri_inception_data)
            if args.findings == "all":
                calc_correlation_coefficient(dmmri_inception_data)
        elif args.encoder == "dinov2":
            if args.findings == "corrcoef":
                calc_correlation_coefficient(dmmri_dinov2_data)
            if args.findings == "all":
                calc_correlation_coefficient(dmmri_dinov2_data)
        elif args.encoder == None:
            # Output normalised metric values for each DMMRI data dictionary
            if args.findings == "normalise":
                print(normalise_metric_values(dict(list(dmmri_inception_data.items())[1:])))
                print(normalise_metric_values(dict(list(dmmri_dinov2_data.items())[1:])))
            # Output graphs for each DMMRI metric
            elif args.findings == "metrics":
                plot_metric_graphs(dmmri_all_data, standard_synth_pcts)
            # Output graphs for each DMMRI normalised metric
            elif args.findings == "normalisedmetrics":
                plot_normalised_metric_graphs(dmmri_all_data, standard_synth_pcts)
            # Output DMMRI metric graph matrix
            elif args.findings == "metricmatrix":
                generate_metric_graph_matrix(dmmri_all_data, standard_synth_pcts)

if __name__ == '__main__':
    main()