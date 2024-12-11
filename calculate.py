import pandas as pd
import numpy as np
from statsmodels.stats.inter_rater import fleiss_kappa

def calculate_fleiss_kappa(matrix):
    """
    Calculate Fleiss' Kappa for inner-annotator agreement from an Excel file.

    Returns:
        float: Fleiss' Kappa value.
    """
    # Calculate Fleiss' Kappa
    kappa = fleiss_kappa(matrix, method='fleiss')

    return kappa

def process_data(file_path, annotator_ids=[], dataset_ids=[]):
    # Load the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path)

    # Ensure the data has the required columns
    required_columns = ["Data ID", "Annotator ID", "Label ID"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
        
    # Filter the DataFrame for the specified annotators
    if len(annotator_ids) != 0:
        df = df[df["Annotator ID"].isin(annotator_ids)]
        if df.empty:
            raise ValueError(f"No data available for annotators: {annotator_ids}")
        
    if len(dataset_ids) != 0:
        df = df[df["Dataset ID"].isin(dataset_ids)]
        if df.empty:
            raise ValueError(f"No data available for datasets: {dataset_ids}")
    
     # Create a pivot table to count the number of annotators assigning each label to each data point
    label_counts = df.pivot_table(
        index="Data ID",
        columns="Label ID",
        values="Annotator ID",
        aggfunc="count",
        fill_value=0
    )
    print(label_counts)
    row_sums = label_counts.sum(axis=1)
    print(type(row_sums))
    for i, v in row_sums.items():
        if v != len(annotator_ids):
            print(i, v)
    matrix = label_counts.to_numpy()
    # print(matrix)
    print(matrix.shape)
    return matrix

if __name__ == '__main__':
    # Example usage
    file_path = "annotations/training/Pilot Study - Du - Iteration2.xlsx"  # Replace with your Excel file path
    annotator_ids = [2, 3, 4] #[2, 4]
    dataset_ids = [41] #[52]
    matrix = process_data(file_path, annotator_ids, dataset_ids)
    kappa_value = calculate_fleiss_kappa(matrix)
    print(f"Fleiss' Kappa: {kappa_value}")