import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse

# Initialising loss data
ganmri10_loss_data = {
    "100% real": [3.884354585, 1.358598612, 0.628641151, 0.178619057, 0.28054988, 0.156474985, 0.126280726, 0.04570445, 0.063098292, 0.032721977, 0.025071275, 0.025451113, 0.013941883, 0.014005613, 0.016696906],
    "50% real, 50% synthetic": [5.536033329, 4.005757794, 0.617330238, 0.514298912, 0.545020962, 0.149958007, 0.267717289, 0.262782387, 0.102709049, 0.107502402, 0.065172702, 0.081478671, 0.011430854, 0.025130068, 0.01961707],
    "25% real, 75% synthetic": [4.854657397, 6.889021158, 2.084724441, 1.446450651, 1.312525284, 0.293182973, 0.257969311, 0.116146003, 0.119198211, 0.092602363, 0.022826678, 0.065354352, 0.027486844, 0.067532882, 0.031318476],
    "100% synthetic": [4.111320053, 0.65433497, 0.473223172, 0.829968207, 0.170292642, 0.171400454, 0.207588488, 0.098987298, 0.152942243, 0.031075068, 0.232847019, 0.077056157, 0.067872486, 0.088301135, 0.048726631]
}
ganmri100_loss_data = {
    "100% real": [4.281215727, 0.294141296, 0.233868387, 0.128635405, 0.0711687, 0.098527305, 0.06112668, 0.046478961, 0.044106062, 0.038397775, 0.02781179, 0.027631726, 0.02379076, 0.019170764, 0.017362426],
    "50% real, 50% synthetic": [4.559810326, 0.370020725, 0.198578127, 0.107705253, 0.090481337, 0.081424235, 0.081021538, 0.056198427, 0.046076448, 0.032974259, 0.028514073, 0.024544405, 0.022276453, 0.021035429, 0.020902273],
    "40% real, 60% synthetic": [6.622271568, 0.798955664, 0.228738207, 0.245206127, 0.197986539, 0.123280559, 0.124042915, 0.084727366, 0.067778171, 0.060199031, 0.04429344, 0.037479992, 0.031071002, 0.025301589, 0.02283859],
    "30% real, 70% synthetic": [6.255630866, 0.737353232, 0.42746691, 0.177006533, 0.176088389, 0.178784842, 0.096276989, 0.064748254, 0.064542702, 0.044390005, 0.027056029, 0.031459505, 0.023427459, 0.021379132, 0.014976247],
    "20% real, 80% synthetic": [4.803307459, 0.597851846, 0.387358621, 0.265314814, 0.157584923, 0.176974051, 0.108154455, 0.047715295, 0.042110102, 0.038985068, 0.025870027, 0.017291105, 0.013763809, 0.009369388, 0.008815302],
    "10% real, 90% synthetic": [5.973773718, 0.55383724, 0.320203383, 0.196291646, 0.195392398, 0.135961285, 0.080699529, 0.081212007, 0.059856105, 0.051845521, 0.044061168, 0.040516923, 0.032038143, 0.027502517, 0.024514136],
    "100% synthetic": [6.190061897, 1.110511743, 0.597303919, 0.386488788, 0.263256865, 0.182324842, 0.096339608, 0.121453243, 0.087791484, 0.075079178, 0.061271388, 0.04472199, 0.040552143, 0.032239854, 0.028314398]
}

def plot_training_loss(loss_data_dict):
    """
    Plots training loss vs. epoch number for different training data ratios.
    
    Parameters:
    - loss_data_dict (dict): Keys are data ratio labels (str), values are lists/arrays of 15 training loss values.
    """
    # Ensure data is in DataFrame format
    epochs = np.arange(1, 16)  # Epochs from 1 to 15
    df = pd.DataFrame(index=epochs)

    for label, losses in loss_data_dict.items():
        if len(losses) != 15:
            raise ValueError(f"Expected 15 loss values for '{label}', but got {len(losses)}.")
        df[label] = losses

    # Plotting values on a line graph
    plt.figure(figsize=(10, 6))
    for column in df.columns:
        plt.plot(df.index, df[column], marker='o', label=column)

    plt.title('Training Loss per Epochs for GANMRI100 Datasets')
    plt.xlabel('Epoch')
    plt.ylabel('Training Loss')
    plt.xticks(epochs)
    plt.legend(title='Training Data Ratio')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

#def plot_segmentation_performance():

def main():
    parser = argparse.ArgumentParser(description="Plot findings of segmentation tasks using Matplotlib")
    parser.add_argument("--findings", type=str, default="both", help="Type of segmentation task findings to plot (e.g. loss, performance).")
    args = parser.parse_args()

    if args.findings == "loss":
        plot_training_loss(ganmri100_loss_data)
    # elif args.findings == "performance":
    #     plot_segmentation_performance()
    # elif args.findings == "both":
    #     plot_training_loss(loss_data)
    #     plot_segmentation_performance()

if __name__ == '__main__':
    main()