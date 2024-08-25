import json
import utils_diff
from tqdm import tqdm

def process(data):
    processed_data = []
    for i in tqdm(range(len(data))):
        sample = data[i]
        edits = utils_diff.get_edit_operations(sample["r_content"], sample["s_content"], split_replace=True, split_sentences=True)
        before_context = sample["r_content"]
        after_context = sample["s_content"]
        r_tokens = utils_diff.tokenize(sample['r_content'])
        s_tokens = utils_diff.tokenize(sample['s_content'])
        # for edit in edits:
        #     print(edit)
        for edit_group in sample["annotations"]:
            category = edit_group['category']
            opis = edit_group['opis']
            min_opi, max_opi = min(opis), max(opis)
            before, after = "", ""
            before_N_tokens, after_N_tokens = 0, 0
            for opi in range(min_opi):
                # count the start position of the diff span
                edit = edits[opi]
                N_tokens = edit['N_words']
                if edit['type'] == 'delete':
                    before_N_tokens += N_tokens
                elif edit['type'] == 'insert':
                    after_N_tokens += N_tokens
                else:
                    before_N_tokens += N_tokens
                    after_N_tokens += N_tokens

            before_start_pos, before_end_pos = 0, 0
            if before_N_tokens >= len(r_tokens):
                before_N_tokens = len(r_tokens)
            for idx in range(before_N_tokens-1, 0, -1): # inverse order
                # find the start position of the diff span
                if is_end_of_sentence(idx, r_tokens):
                    before_start_pos = idx + 1
                    break
            # print("before_prior_subsentence", utils_diff.untokenize(r_tokens[:before_start_pos]))
            after_start_pos, after_end_pos = 0, 0
            if after_N_tokens >= len(s_tokens):
                after_N_tokens = len(s_tokens)
            for idx in range(after_N_tokens-1, 0, -1):
                # print(idx, len(s_tokens))
                if is_end_of_sentence(idx, s_tokens):
                    after_start_pos = idx + 1
                    break
            # print("after_prior_subsentence", utils_diff.untokenize(s_tokens[:after_start_pos]))
            
            before_diff_span_range, after_diff_span_range = [before_N_tokens, before_N_tokens], [after_N_tokens, after_N_tokens]
            before_list, after_list = [], []
            for opi in range(min_opi, max_opi+1):
                edit = edits[opi]
                N_tokens = edit['N_words']
                if edit['type'] == 'delete':
                    before_list.append(edit['delete'])
                    before_N_tokens += N_tokens
                    before_diff_span_range[1] += N_tokens
                elif edit['type'] == 'insert':
                    after_list.append(edit['insert'])
                    after_N_tokens += N_tokens
                    after_diff_span_range[1] += N_tokens
                else:
                    before_list.append(edit['text'])
                    after_list.append(edit['text'])
                    before_N_tokens += N_tokens
                    before_diff_span_range[1] += N_tokens
                    after_N_tokens += N_tokens
                    after_diff_span_range[1] += N_tokens

            before, after = utils_diff.untokenize(before_list), utils_diff.untokenize(after_list)
            # print("before_diff_span", before)
            # print("after_diff_span", after)

            before_sentence_token_range, after_sentence_token_range = [before_start_pos, 0], [after_start_pos, 0]
            for idx in range(before_N_tokens-1, len(r_tokens)): # inverse order
                # find the end position of the diff span
                if is_end_of_sentence(idx, r_tokens):
                    before_end_pos = idx + 1  # left closed, right open [start, end)
                    break
            before_sentence_token_range[1] = before_end_pos
            # print("before_rear_subsentence", utils_diff.untokenize(r_tokens[before_start_pos:before_end_pos]))

            for idx in range(after_N_tokens-1, len(s_tokens)):
                if is_end_of_sentence(idx, s_tokens):
                    after_end_pos = idx + 1
                    break
            after_sentence_token_range[1] = after_end_pos 
            # print("after_rear_subsentence", utils_diff.untokenize(r_tokens[after_start_pos:after_end_pos]))
            
            before_sentence = utils_diff.untokenize(r_tokens[before_start_pos: before_end_pos])
            after_sentence = utils_diff.untokenize(s_tokens[after_start_pos: after_end_pos])
            # if before_sentence in before_sentence_mapping.keys():
            #     temp_after_sentence = before_sentence_mapping[before_sentence]
            #     if temp_after_sentence in after_sentence:
            #         before_sentence_mapping[before_sentence] = after_sentence
            # else:
            #     before_sentence_mapping[before_sentence] = after_sentence

            # print("\n>>===========================")
            # print("context", before_context)
            # print("before:", before)
            # print(" after:", after)
            # # print("before_token_range:", before_token_range)
            # # print(r_tokens[before_token_range[0]: before_token_range[1]])
            # # print("after_token_range:", after_token_range)
            # # print(s_tokens[after_token_range[0]: after_token_range[1]])

            # print("before_sentence:", before_sentence)
            # print(" after_sentence:", after_sentence)
            # # print("category:", category)
            # print("===========================<<\n")
            # input()
            processed_data.append({
                "before_context": sample['r_content'], 
                "after_context": sample['s_content'], 
                "before_sentence": before_sentence,
                "after_sentence": after_sentence,
                "before": before,
                "after": after,
                "before_diff_span_range": before_diff_span_range,
                "after_diff_span_range": after_diff_span_range,
                "before_sentence_token_range": before_sentence_token_range,
                "after_sentence_token_range": after_sentence_token_range,
                "label": category
            })
        # for key, value in before_sentence_mapping.items():
        #     print("\n-----------------")
        #     print("key", key)
        #     print("value", value)

        #     print("-----------------\n")
        # for d in processed_data:
        #     before_sentence = d['before_sentence']
        #     d['after_sentence'] = before_sentence_mapping[before_sentence]

            # print("context", d['context'])
            # print("before_sentence", d['before_sentence'],)
            # print("after_sentence", d['after_sentence'],)
            # print("before", d['before'],)
            # print("after", d['after'],)
            # print("before_sentence_token_range", d['before_sentence_token_range'],)
            # print("label", d['label'])
            # print("=========================\n\n")

    return processed_data

def subsumes(list1, list2):
    return set(list2).issubset(set(list1))

def is_end_of_sentence(position, tokens):
    if tokens[position] == '.' or tokens[position] == '!' or tokens[position] == '?':
        return True
    return False
        


processed_data = []
with open("data/swipe_train.json", "r") as f: # See: data/swipe_val.json, data/swipe_test_id.json, data/swipe_test_ood.json for the validation, in-domain test, and out-of-domain test sets
    swipe_train = json.load(f)
    data = process(swipe_train)
    processed_data.extend(data)

with open("data/swipe_val.json", "r") as f:
    swipe_val = json.load(f)
    data = process(swipe_val)
    processed_data.extend(data)

# with open("data/sample.json", "r") as f:
#     swipe_val = json.load(f)
#     data = process(swipe_val)
#     processed_data.extend(data)
    
print("Number of edits:", len(processed_data))
with open('processed_swipe_data.json', 'w') as json_file:
    json.dump(processed_data, json_file, indent=4)