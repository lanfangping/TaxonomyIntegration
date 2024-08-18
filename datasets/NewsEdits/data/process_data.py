import pandas as pd
import json

def read_csv(filepath):
    return pd.read_csv(filepath, engine='python')

def read_json(filepath):
    data = json.load(open(filepath))
    return data

def save_json(data, outpath):
    with open(outpath, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def store_csv(data, outpath):
    df = pd.DataFrame(data)
    df.to_csv(outpath)  

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

def process(filepath):
    data = read_json(filepath)
    edit_pairs = []
    for key, value in data.items():
        sentence1 = value['sentence-1']
        sentence2 = value['sentence-2']
        sentence1_tokens = sentence1.split()
        sentence2_tokens = sentence2.split()

        # discard short pairs
        if len(sentence1_tokens) < 10 or len(sentence2_tokens) < 10:
            continue

        for k, edit in value['edits-combination-0'].items():
            intention = edit['intention']
            token_indices1 = edit['sentence-1-token-indices']
            token_indices2 = edit['sentence-2-token-indices']

            if token_indices1 is None:
                before = sentence1
                # after = " ".join(sentence2_tokens[:token_indices2[0]]) + 

                if token_indices2[0] > 0:
                    pre_token = sentence2_tokens[token_indices2[0]-1]
                else:
                    pre_token = None
                
                if token_indices2[1] == len(sentence2_tokens):
                    post_token = None
                else:
                    post_token = sentence2_tokens[token_indices2[1]]

                # print("pre_token", pre_token)
                # print("post_token", post_token)
                insert_point = 0
                for i in range(len(sentence1_tokens)-1):
                    token_i = sentence1_tokens[i]
                    token_i_plus_1 = sentence1_tokens[i+1]
                    if (pre_token and pre_token in token_i) or (post_token and post_token in token_i_plus_1):
                        insert_point = i+1
                    
                after = " ".join(sentence1_tokens[:insert_point]) + " " + \
                        " ".join(sentence2_tokens[token_indices2[0]: token_indices2[1]]) + " " + \
                        " ".join(sentence1_tokens[insert_point:])
                # print("before", before)
                # print("after", after)
            elif token_indices2 is None: 
                before = sentence1
                after = " ".join(sentence1_tokens[:token_indices1[0]]) + " " + \
                        " ".join(sentence1_tokens[token_indices1[1]:])
                # print("before", before)
                # print("after", after)
            else:
                before = sentence1
                after = " ".join(sentence1_tokens[:token_indices1[0]]) + " " + \
                        " ".join(sentence2_tokens[token_indices2[0]: token_indices2[1]]) + " " + \
                        " ".join(sentence1_tokens[token_indices1[1]:])
                # print("before", before)
                # print("after ", after)

            edit_pairs.append({
                'before': before,
                'after': after
            })
            # input()
    return edit_pairs


if __name__ == '__main__':
    # sentence1 = """< p > A Massachusetts police officer described as a " great family man and officer " died Sunday after a man attacked him with a rock , then took the cop 's gun and shot him in the head and chest , officials said ."""
    # sentence2 = """< p > A Massachusetts police officer and an elderly woman were killed Sunday after a suspect attacked the officer with a rock , took his gun and shot him in the head and chest , officials said ."""

    # sentence1 = """< p > According to the letter , a uniformed Border Patrol agent noticed a group on the Rio Grande River flood plain south of the Tornillo , Texas , Port of Entry , taking photos of the holding facility ."""
    # sentence2 = """The mayor and his security detail were spotted taking photos by a Border Patrol agent on the Rio Grande River flood plain south of the Tornillo , Texas , Port of Entry ."""

    # sentence1 = """< p > Lopes was arrested and rushed to a hospital with injuries that were not life - threatening ."""
    # sentence2 = """< p > Lopes was arrested and taken to a hospital with injuries that were not life - threatening ."""

    # filepath = './macthed_sentences.csv'
    # outpath = './macthed_sentences_formatted.csv'
    # df = read_csv(filepath)
    # data = process_data_to_newsedits_format(df)
    # save_json(data, outpath)

    filepath = './newsedits_edits.json'
    data_dict = process(filepath)
    store_csv(data_dict, './newsedits_edits_pairs.csv')

