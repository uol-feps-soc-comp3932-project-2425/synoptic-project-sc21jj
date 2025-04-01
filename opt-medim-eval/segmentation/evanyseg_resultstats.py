import numpy as np
import csv
import argparse

# Function to read data from a CSV file
def read_data_from_file(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row (true_dice,preds_dices)
        for row in reader:
            true_dice = float(row[0])  # Convert the first column to float
            preds_dice = float(row[1])  # Convert the second column to float
            data.append((true_dice, preds_dice))
    return data

# Function to calculate pairwise differences
def calculate_pairwise_differences(data):
    return [truedice - preddice for truedice, preddice in data]

# Function to calculate the variance of the differences
def calculate_variance(differences):
    return np.var(differences)

# Function to calculate the average of the differences
def calculate_average(differences):
    return np.mean(differences)

# Function to calculate the average of the true DICE scores
def calculate_average_true_dice(data):
    true_dice_values = [truedice for truedice, _ in data]
    return np.mean(true_dice_values)

# Function to calculate the average of the predicted DICE scores
def calculate_average_predicted_dice(data):
    preds_dice_values = [preds for _, preds in data]
    return np.mean(preds_dice_values)

# Function to calculate the variance of the true DICE scores
def calculate_variance_true_dice(data):
    true_dice_values = [truedice for truedice, _ in data]
    return np.var(true_dice_values)

# Function to calculate the variance of the predicted DICE scores
def calculate_variance_predicted_dice(data):
    preds_dice_values = [preds for _, preds in data]
    return np.var(preds_dice_values)

# Set up the command line argument parser
parser = argparse.ArgumentParser(description="Calculate relevant statistics based on true_dice and preds_dice values.")
parser.add_argument("filename", help="Path to the CSV file containing the data")

# Parse command line arguments
args = parser.parse_args()

# Read data from the provided file
data = read_data_from_file(args.filename)

# Calculate pairwise differences
differences = calculate_pairwise_differences(data)

# Calculate variance and average of differences
variance_differences = calculate_variance(differences)
average_differences = calculate_average(differences)

# Calculate average and variance of true DICE scores
average_true_dice = calculate_average_true_dice(data)
variance_true_dice = calculate_variance_true_dice(data)

# Calculate average and variance of predicted DICE scores
average_predicted_dice = calculate_average_predicted_dice(data)
variance_predicted_dice = calculate_variance_predicted_dice(data)

# Print the results
print("Variance of the differences:", variance_differences)
print("Average of the differences:", average_differences)

print("\nAverage of the true DICE scores:", average_true_dice)
print("Variance of the true DICE scores:", variance_true_dice)

print("\nAverage of the predicted DICE scores:", average_predicted_dice)
print("Variance of the predicted DICE scores:", variance_predicted_dice)