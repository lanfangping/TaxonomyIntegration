import os
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedShuffleSplit

# Define the sampling function
def sample_data(group, n=1, random_state=42):
    return group.sample(n=min(len(group), n), random_state=random_state)

def sampling(df, repo, n_sampels_pilot_study,n_sampels_pilot_study_list, n_samples_comparing_group, random_seed, group_by=['domain', 'label']):
    """
    IteraTer: random_seed=41, n_sampels_pilot_study=5, n_sampels_pilot_study_list=[1, 2, 2], n_samples_comparing_group=71
    """
    # Sample n rows per 'domain' and 'label' combination with a random seed
    sampled_df = df.groupby(group_by).apply(sample_data, n=n_sampels_pilot_study, random_state=random_seed).reset_index(drop=True)

    print(sampled_df)
    # Get the indices of the sampled data
    sampled_indices = sampled_df.index

    # Drop the sampled data to get the remaining data
    remaining_df = df.drop(sampled_indices)

    remaining_df = remaining_df.reset_index(drop=True)

    # Convert DataFrame to JSON Lines format and save to a file
    sampled_df.to_json(f"../sampling/{repo}/pilot_study_{repo.lower()}.json", orient='records', lines=True)

    for idx, n_samples in enumerate(n_sampels_pilot_study_list):
        # Sample n rows per 'domain' and 'label' combination with a random seed
        sampled_iter_df = sampled_df.groupby(['domain', 'label']).apply(sample_data, n=n_samples, random_state=random_seed).reset_index(drop=True)

        sampled_iter_df.to_json(f"../sampling/{repo}/pilot_study_{repo.lower()}_iter{idx+1}.json", orient='records', lines=True)

        # Get the indices of the sampled data
        sampled_iter_indices = sampled_iter_df.index

        # Drop the sampled data to get the remaining data
        sampled_df = sampled_df.drop(sampled_iter_indices)
        # Reset the index
        sampled_df = sampled_df.reset_index(drop=True)

    ## dataset for comparing group
    # Sample n rows per 'domain' and 'label' combination with a random seed
    comparing_df = remaining_df.groupby(['domain', 'label']).apply(sample_data, n=n_samples_comparing_group, random_state=random_seed).reset_index(drop=True)
    comparing_df.to_json(f"../sampling/{repo}/comparing_group_{repo.lower()}.json", orient='records', lines=True)


def straified_sampling(data, x_labels, y_label, n_small, repo):
    # # Example dataset with "before", "after", and "label" columns
    # data = pd.DataFrame({
    #     'before': np.random.randn(1000),
    #     'after': np.random.randn(1000),
    #     'label': np.random.randint(0, 3, size=1000)  # Example labels 0, 1, 2
    # })

    # # Separate the features (before, after) and labels
    # X = data[['before', 'after']].values
    # y = data['label'].values
    X = data[x_labels].values
    y = data[y_label].values

    # Specify the size of the smaller dataset you want to sample
    # n_small = 200  # for example, sampling 200 points

    # Using StratifiedShuffleSplit to sample based on the "label" distribution
    stratified_split = StratifiedShuffleSplit(n_splits=1, train_size=n_small)

    # Perform the split
    for train_idx, _ in stratified_split.split(X, y):
        sampled_X = X[train_idx]
        sampled_y = y[train_idx]

    # Create a DataFrame for the sampled dataset
    sampled_data = pd.DataFrame(sampled_X, columns=x_labels)
    sampled_data[y_label] = sampled_y

    # Show the sampled data
    print(sampled_data.head())

    # Optional: Check the label distribution to ensure it matches the original distribution
    original_distribution = data[y_label].value_counts(normalize=True)
    sampled_distribution = sampled_data[y_label].value_counts(normalize=True)

    print("Original Label Distribution:")
    print(original_distribution)

    print("\nSampled Label Distribution:")
    print(sampled_distribution)
    sampled_data.to_json(os.path.join(f"./{repo}", f"comparing_group_{repo.lower()}.json"), orient='records', lines=True)

if __name__ == '__main__':
    # file_path = './processed/processed_sent_level.json'
    # # Step 1: Verify the file path
    # if not os.path.exists(file_path):
    #     print("File not found:", file_path)
    # else:
    #     print("File found:", file_path)

    #     df = pd.read_json(file_path, lines=True)

    #     sampling(df, "arXivEdits", 5, [1, 2, 2], n_samples_comparing_group=)

    file_path = "./IteraTeR/remaining_iterater.json"
    x_labels = ['doc_id', 'context', 'domain', 'before_edit', 'after_edit', 'start_sent_pos', 'end_sent_pos', 'raw_intents']
    y_label = 'label'
    n_small = 1000
    repo='IteraTeR'

    # file_path = "./arXivEdits/remaining_arxivedits.json"
    # x_labels = ['before', 'after']
    # y_label = 'label'
    # n_small = 1000
    # repo='arXivEdits'
    data = pd.read_json(file_path, lines=True)
    straified_sampling(data, x_labels, y_label, n_small, repo)