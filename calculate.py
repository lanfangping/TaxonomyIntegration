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

def get_pivot_table(df, dataset_ids=[]):
    if len(dataset_ids) != 0:
        df = df[df["Dataset ID"].isin(dataset_ids)]
        if df.empty:
            raise ValueError(f"No data available for datasets: {dataset_ids}")
        
    # Step 1: Set 'Dataset ID' as a categorical column with the specified order
    # df['Dataset ID'] = pd.Categorical(df['Dataset ID'], categories=dataset_ids, ordered=True)

    # Step 2: Sort by 'Dataset ID' first, then '37' column, then '39' column
    # df_sorted = df.sort_values(by=['Dataset ID', 37, 39], ascending=[True, False, True])
        
    # Sort by 'Column A' first, then by 'Column B'
    df = df.sort_values(by=['File Name', 'Data ID', 'Annotator ID'], ascending=[True, True, True])
    df['ID'] = pd.factorize(df['Data ID'])[0]
    print(df)
    # Ensure the data has the required columns
    required_columns = ["ID", "Data ID", "Annotator ID", "Label ID"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    
    # Create a pivot table to count the number of annotators assigning each label to each data point
    df_pivot_table = pd.pivot_table(
        data=df,
        index=["ID", "Data ID"],
        columns="Label ID",
        values="Annotator ID",
        aggfunc="count",
        fill_value=0
    )
    print(df_pivot_table)
    # row_sums = label_counts.sum(axis=1)
    # print(type(row_sums))
    # for i, v in row_sums.items():
    #     if v != len(annotator_ids):
    #         print(i, v)
    # # Find the rows where any column contains the value `3`
    # filtered_rows = df_pivot_table[df_pivot_table.eq(3).any(axis=1)]

    # Filter rows with exactly 3 occurrences of 1
    filtered_rows = df_pivot_table[df_pivot_table.eq(1).sum(axis=1) == 3]

    # Extract the 'Data ID' for these rows
    

    id_dataid_mapping = {d_id:data_id for d_id, data_id in filtered_rows.index.tolist()}
    # print(list(data_ids))
    return id_dataid_mapping


def process_data(file_path, annotator_ids=[], dataset_ids=[], n_samples=None, seed=10):
    # Load the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path)
    # print("Unique Data IDs:", df["Data ID"].nunique())  # Should match the number of rows in the pivot table
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
        
    if n_samples is not None:
        # df = df.sample(n=n_samples, random_state=seed)
        sampled_data_ids = df["Data ID"].drop_duplicates().sample(n=n_samples, random_state=seed)

        # Extract rows corresponding to the sampled Data IDs
        df = df[df["Data ID"].isin(sampled_data_ids)]

    # print(df.head())
    # print(df.shape)

    # # Check the unique values of "Data ID" and "Label ID" in the original dataframe
    # print("Unique Data IDs:", df["Data ID"].nunique())  # Should match the number of rows in the pivot table

    # print("Unique Label IDs:", df["Label ID"].nunique())  # Should match the number of columns in the pivot table

    # # Check for missing values
    # print("Missing values in Data ID:", df["Data ID"].isna().sum())
    # print("Missing values in Label ID:", df["Label ID"].isna().sum())



    # Create a pivot table to count the number of annotators assigning each label to each data point
    label_counts = df.pivot_table(
        index="Data ID",
        columns="Label ID",
        values="Annotator ID",
        aggfunc="count",
        fill_value=0
    )
    # print(label_counts)
    row_sums = label_counts.sum(axis=1)
    # print(type(row_sums))
    for i, v in row_sums.items():
        if v != len(annotator_ids) and len(annotator_ids) != 0:
            print(i, v)
    matrix = label_counts.to_numpy()
    # print(matrix)
    print(matrix.shape)
    print(matrix.sum())

        # Inspect the pivot table
    # print("Pivot table head:\n", label_counts.head())

    # # Compare shapes
    # print("Original DataFrame shape:", df.shape)
    # print("Pivot table shape:", label_counts.shape)
    return matrix

# def venn_data(df1, df2):

def get_distribution(df):
    # Step 2: Remove duplicates for the same 'Data ID', 'Label ID', and 'Label Name'
    df = df.drop_duplicates(subset=['Data ID', 'Label ID', 'Label Name'])

    label_distribution = df.groupby(['Label ID', 'Label Name']).size().reset_index(name='Count')
    print(label_distribution)

if __name__ == '__main__':
    # Example usage
    file_path = "annotations/2annotator/Comparing Group - Ours - Iter.xlsx"  # Replace with your Excel file path
    annotator_ids = [] #[2, 4]
    dataset_ids = [] #[52]
    n_samples = None
    seed = 25
    matrix = process_data(file_path, annotator_ids, dataset_ids, n_samples, seed)
    kappa_value = calculate_fleiss_kappa(matrix)
    print(f"Fleiss' Kappa: {kappa_value}")

    # # VENN data
    # file_path= "annotations/2annotator/Comparing Group - Ours - ArXiv.xlsx"
    # df1 = pd.read_excel(file_path)
    # dataset_ids = []
    # id_dataid_mapping1 = get_pivot_table(df1, dataset_ids)

    # file_path= "annotations/2annotator/Comparing Group - Ruan - ArXiv.xlsx"
    # df2 = pd.read_excel(file_path)
    # dataset_ids = []
    # id_dataid_mapping2 = get_pivot_table(df2, dataset_ids)

    # print("#total disagree with ours:", len(id_dataid_mapping1))
    # print("#total disagree with Du:", len(id_dataid_mapping2))

    # set1 = set(id_dataid_mapping1.keys())
    # set2 = set(id_dataid_mapping2.keys())
    # overlapping = set1.intersection(set2)
    # agree_our_disagree_du = set1.difference(set2)
    # agree_du_disagree_our = set2.difference(set1)

    # print("Overlapping ", len(overlapping))   
    # print("disagree_our_but_not_ruan ", len(agree_our_disagree_du)) 
    # print("disagree_ruan_but_not_ours ", len(agree_du_disagree_our)) 

    # file_path= "annotations/2annotator/Comparing Group - Ours - ArXiv.xlsx"
    # df_ours = pd.read_excel(file_path)
    # print("Overlapping on ours")
    # data_ids = [id_dataid_mapping1[id_] for id_ in overlapping]
    # filtered_df = df_ours[df_ours['Data ID'].isin(data_ids)]
    # # Step 2: Group by 'Label ID' and 'Label Name' and calculate counts
    # get_distribution(filtered_df)
    # print()

    # # Step 1: Filter rows based on the Data ID list
    # print("disagree_our_but_not_ruan")
    # data_ids = [id_dataid_mapping1[id_] for id_ in agree_our_disagree_du]
    # filtered_df = df_ours[df_ours['Data ID'].isin(data_ids)]
    # # Step 2: Group by 'Label ID' and 'Label Name' and calculate counts
    # get_distribution(filtered_df)
    # print()

    # print("Overlapping on Ruan")
    # file_path= "annotations/2annotator/Comparing Group - Ruan - ArXiv.xlsx"
    # df_du = pd.read_excel(file_path)
    # data_ids = [id_dataid_mapping2[id_] for id_ in overlapping]
    # filtered_df = df_du[df_du['Data ID'].isin(data_ids)]
    # # Step 2: Group by 'Label ID' and 'Label Name' and calculate counts
    # get_distribution(filtered_df)
    # print()

    # print("disagree_ruan_but_not_ours")
    # # Step 1: Filter rows based on the Data ID list
    # data_ids = [id_dataid_mapping2[id_] for id_ in agree_du_disagree_our]
    # # print(len(data_ids))
    # filtered_df = df_du[df_du['Data ID'].isin(data_ids)]
    # # print(filtered_df)
    # # Step 2: Group by 'Label ID' and 'Label Name' and calculate counts
    # get_distribution(filtered_df)
    # print()