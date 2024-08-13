import json
import utils_diff
from tqdm import tqdm

processed_data = []
with open("data/swipe_train.json", "r") as f: # See: data/swipe_val.json, data/swipe_test_id.json, data/swipe_test_ood.json for the validation, in-domain test, and out-of-domain test sets
    swipe_train = json.load(f)
    for i in tqdm(range(len(swipe_train))):
        sample = swipe_train[i]
        edits = utils_diff.get_edit_operations(sample["r_content"], sample["s_content"], split_replace=True, split_sentences=True)
        # for edit in edits:
        #     print(edit)
        for edit_group in sample["annotations"]:
            category = edit_group['category']
            opis = edit_group['opis']
            min_opi, max_opi = min(opis), max(opis)
            before_sentence, after_sentence = "", ""
            before, after = "", ""
            before_N_tokens, after_N_tokens = 0, 0

            for opi in range(min_opi):
                edit = edits[opi]
                N_tokens = edit['N_words']
                if edit['type'] == 'delete':
                    before_N_tokens += N_tokens
                elif edit['type'] == 'insert':
                    after_N_tokens += N_tokens
                else:
                    before_N_tokens += N_tokens
                    after_N_tokens += N_tokens
            before_token_range, after_token_range = [before_N_tokens, before_N_tokens], [after_N_tokens, after_N_tokens]
            for opi in range(min_opi, max_opi+1):
                edit = edits[opi]
                N_tokens = edit['N_words']
                if edit['type'] == 'delete':
                    before += edit['delete']
                    before_token_range[1] += N_tokens
                elif edit['type'] == 'insert':
                    after += edit['insert']
                    after_token_range[1] += N_tokens
                else:
                    before += edit['text']
                    after += edit['text']
                    before_token_range[1] += N_tokens
                    after_token_range[1] += N_tokens
            # print("\n>>===========================")
            # print("before:", before)
            # print(" after:", after)
            # print("before_token_range:", before_token_range)
            # r_tokens = utils_diff.tokenize(sample['r_content'])
            # print(r_tokens[before_token_range[0]: before_token_range[1]])
            # s_tokens = utils_diff.tokenize(sample['s_content'])
            # print("after_token_range:", after_token_range)
            # print(s_tokens[after_token_range[0]: after_token_range[1]])

            # print("===========================<<\n")

            processed_data.append({
                "before_content": sample['r_content'],
                "after_content": sample['s_content'],
                "before": before,
                "after": after,
                "before_token_range": before_token_range,
                "after_token_range": after_token_range
            })
print("Number of edits:", len(processed_data))
with open('processed_swipe_data.json', 'w') as json_file:
    json.dump(processed_data, json_file, indent=4)