import json
import pandas as pd

def read_json(filepath):
    data = json.load(open(filepath))
    return data

def store_csv(data, outpath):
    df = pd.DataFrame(data)
    df.to_csv(outpath)  

def process(filepath):
    data = read_json(filepath)
    edit_pairs = []
    for key, value in data.items():
        sentence1 = value['sentence-1']
        sentence2 = value['sentence-2']
        sentence1_tokens = sentence1.split()
        sentence2_tokens = sentence2.split()

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
                'after': after,
                'label': intention
            })
            # input()
    return edit_pairs

if __name__ == '__main__':
    outpath = './data/edits/edits_processed.csv'

    data = []
    dev_data = process('./data/edits/dev.json')
    test_data = process('./data/edits/test.json')
    train_data = process('./data/edits/train.json')
    
    data.extend(dev_data)
    data.extend(test_data)
    data.extend(train_data)

    store_csv(data, outpath)