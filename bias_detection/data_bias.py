from aequitas.group import Group
from aequitas.bias import Bias
import pandas as pd
import os

def detect_data_bias(data, protected_columns=['Gender']):
    """
    Detects bias in the input data using Aequitas.

    Parameters:
    data (pd.DataFrame): Input data to be analyzed
    protected_columns (list): List of protected attribute columns

    Returns:
    pd.DataFrame: Bias detection results
    """
    # Define Bias attributes
    bias_attributes = [
        ('Gender', 'binary'),
        ('Age', 'numeric'),
        ('SSN', 'numeric'),  # Note: SSN is not a perfect proxy for socioeconomic status, but it can be used as a rough estimate
        ('Address', 'categorical'),  # Note: Address can be used as a proxy for geographic location
        ('Code_Description', 'categorical'),  # Note: Code_Description can be used as a proxy for specific medical conditions
        ('Previous_Symptoms', 'categorical'),  # Note: Previous_Symptoms can be used as a proxy for specific health conditions
        ('Previous_Diagnosis', 'categorical'),  # Note: Previous_Diagnosis can be used as a proxy for specific medical conditions
        ('Current_Medication', 'categorical')  # Note: Current_Medication can be used as a proxy for specific treatment plans
    ]

    # Create an Aequitas Group object
    g = Group(data)
    bias_results = {}
    for attribute, attribute_type in bias_attributes:
        bias_results[attribute] = g.bias_imbalance(groupby=[attribute], custom_protected=protected_columns)

    return bias_results

if __name__ == "__main__":
    # Get the absolute path to the current directory
    # current_dir = os.path.dirname(os.path.abspath(__file__))

    # # Construct the absolute path to the CSV file
    # csv_path = os.path.join(os.path.dirname(current_dir), 'data', 'Synthetic_Data.csv')

    # # Read the CSV file
    # data = pd.read_csv(csv_path)

    data=pd.read_csv('..\data\Synthetic_Data.csv')
    df = pd.DataFrame(data)
    
    bias_attributes = [
        ('Gender', 'binary'),
        ('Age', 'numeric'),
        ('SSN', 'numeric'),  # Note: SSN is not a perfect proxy for socioeconomic status, but it can be used as a rough estimate
        ('Address', 'categorical'),  # Note: Address can be used as a proxy for geographic location
        ('Code_Description', 'categorical'),  # Note: Code_Description can be used as a proxy for specific medical conditions
        ('Previous_Symptoms', 'categorical'),  # Note: Previous_Symptoms can be used as a proxy for specific health conditions
        ('Previous_Diagnosis', 'categorical'),  # Note: Previous_Diagnosis can be used as a proxy for specific medical conditions
        ('Current_Medication', 'categorical')  # Note: Current_Medication can be used as a proxy for specific treatment plans
    ]

    bias_results = detect_data_bias(df)
    for attribute, result in bias_results.items():
        print(f"Bias results for {attribute}:")
        print(result.bias)
        print()
