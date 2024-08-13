import pandas as pd
import json

def read_csv(filepath):
    return pd.read_csv(filepath, engine='python')

def save_json(data, outpath):
    with open(outpath, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def process_data_to_newsedits_format(df):
    data_dict = {}
    for row_idx, row in df.iterrows():
        data_dict[row_idx] = {
            "easy-or-hard": "easy",
            "sentence-pair-index": row_idx,
            "sentence-1": f"{row['sentence1']}",
            "sentence-2": f"{row['sentence2']}",
            "edits-combination-0": {},
            "edits-combination-1": {},
            "edits-combination-2": {},
            "arxiv-id": row_idx,
            "sentence-1-level": "simple",
            "sentence-2-level": "complex"
        }
    return data_dict


if __name__ == '__main__':
    # sentence1 = """< p > A Massachusetts police officer described as a " great family man and officer " died Sunday after a man attacked him with a rock , then took the cop 's gun and shot him in the head and chest , officials said ."""
    # sentence2 = """< p > A Massachusetts police officer and an elderly woman were killed Sunday after a suspect attacked the officer with a rock , took his gun and shot him in the head and chest , officials said ."""

    # sentence1 = """< p > According to the letter , a uniformed Border Patrol agent noticed a group on the Rio Grande River flood plain south of the Tornillo , Texas , Port of Entry , taking photos of the holding facility ."""
    # sentence2 = """The mayor and his security detail were spotted taking photos by a Border Patrol agent on the Rio Grande River flood plain south of the Tornillo , Texas , Port of Entry ."""

    # sentence1 = """< p > Lopes was arrested and rushed to a hospital with injuries that were not life - threatening ."""
    # sentence2 = """< p > Lopes was arrested and taken to a hospital with injuries that were not life - threatening ."""

    filepath = './macthed_sentences.csv'
    outpath = './macthed_sentences_formatted.csv'
    df = read_csv(filepath)
    data = process_data_to_newsedits_format(df)
    save_json(data, outpath)