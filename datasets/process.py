import json

def read_json(filename):
    data = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            data.append(json.loads(line))
    return data

def save_jsonl(filename, data):
    with open(filename, "w") as f:
        for element in data:
            f.write(f"{element}\n")


def find_edit_position(target, start_sent_indexs):
    left, right = 0, len(start_sent_indexs) - 1
    
    # Binary search to find the point
    while left <= right:
        mid = left + (right - left) // 2
        
        if start_sent_indexs[mid] == target:
            return mid
        
        elif start_sent_indexs[mid] < target:
            left = mid + 1
        
        else:
            right = mid - 1
    return left

def process_sent(data):
    """
    process sentence-level edit from the doc-level revisions
    """
    processed_data = []
    for element in data:
        doc_id = element['doc_id']
        context = element['before_revision']

        try:
            domain = element['domain']
        except:
            print("Missing domain")
            domain = None            

        edits = element['edit_actions']
        sents_char_pos = element['sents_char_pos']

        for edit in edits:
            before = edit['before']
            after = edit['after']

            start_char_pos = edit['start_char_pos']
            end_char_pos = edit['end_char_pos']

            start_char_in_sent = find_edit_position(start_char_pos, sents_char_pos)
            if start_char_in_sent != 0:
                start_char_in_sent = start_char_in_sent - 1
            start_sent_pos = sents_char_pos[start_char_in_sent]

            end_char_in_sent = find_edit_position(end_char_pos, sents_char_pos)
            if end_char_in_sent == len(sents_char_pos):
                end_sent_pos = len(context)
            else:
                end_sent_pos = sents_char_pos[end_char_in_sent]

            if before is None or before == 'null':
                before_edit = context[start_sent_pos: end_sent_pos]
            else:
                before_edit = context[start_sent_pos: start_char_pos] + before + context[end_char_pos: end_sent_pos]
            if after is None or after == 'null':
                after_edit = context[start_sent_pos: start_char_pos] + context[end_char_pos: end_sent_pos]
            else:
                after_edit = context[start_sent_pos: start_char_pos] + after + context[end_char_pos: end_sent_pos]
                    
            processed_data.append({
                "doc_id": doc_id,
                "context": context,
                "domain": domain,
                "before_edit": before_edit,
                "after_edit": after_edit,
                "label": edit["major_intent"],
                "raw_intents": edit["raw_intents"]
            })
            # print("sents_char_pos", sents_char_pos)
            # print('char_pos', start_char_pos, end_char_pos)
            # print("char_in_sent", start_char_in_sent, end_char_in_sent)
            # print("pos in sent:", start_sent_pos, end_sent_pos)
            # print('before_edit:\n', before_edit)
            # print('\nafter_edit:\n', after_edit)
            # input()
    return processed_data

if __name__ == '__main__':
    filename = './IteraTeR/human_doc_level/test.json'
    data = read_json(filename)
    processed_data = process_sent(data)
    save_jsonl('./IteraTeR/human_doc_level/processed_test.json', processed_data)