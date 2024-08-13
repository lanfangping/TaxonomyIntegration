import pandas as pd
import requests
import copy
from bs4 import BeautifulSoup
from tqdm import tqdm

category_mapping = 	{	
    'counter-vandalism':0, 
    'fact-update': 1, 
    'refactoring':2, 
    'copy-editing':3, 
    'other':4, 
    'wikification':5, 
    'vandalism':6, 
    'simplification':7, 
    'elaboration':8, 
    'verifiability':9, 
    'process':10, 
    'clarification':11,
    'disambiguation':12, 
    'point-of-view':13
}

labelid_mapping = 	{	
    0: 'counter-vandalism', 
    1: 'fact-update', 
    2: 'refactoring', 
    3: 'copy-editing', 
    4: 'other', 
    5: 'wikification', 
    6: 'vandalism', 
    7: 'simplification', 
    8: 'elaboration', 
    9: 'verifiability', 
    10: 'process', 
    11: 'clarification',
    12: 'disambiguation', 
    13: 'point-of-view'
}

def read_csv(filepath):
    df = pd.read_csv(filepath)
    return df

def store_csv(data, outpath):
    df = pd.DataFrame(data)
    df.to_csv(outpath)  

def read_data(df):
    data = []
    for row_idx, row in df.iterrows():
        rev_id = row['rev_id']
        labels_span = row['labels']
        if pd.isna(labels_span):
            continue

        labels = []
        if ',' in labels_span:
            items = labels_span.split(',')
            for item in items:
                label_id = int(item.strip())
                labels.append(labelid_mapping[label_id])
        else:
            label_id = int(labels_span.strip())
            labels.append(labelid_mapping[label_id])

        data.append({
            "rev_id": rev_id,
            "labels": labels
        })
        # print({
        #     "rev_id": rev_id,
        #     "labels": labels
        # })
    return data

# def read_edits(data):
#     for row in data:
#         rev_id = row['rev_id']
#         link = f"https://en.wikipedia.org/wiki/WP:Labels?diff={rev_id}"

def get_wikipedia_revision(diff_url):
    response = requests.get(diff_url)
    if response.status_code != 200:
        raise Exception("Failed to load page")

    soup = BeautifulSoup(response.content, 'html.parser')
    diff_tables = soup.find_all('table', class_='diff')

    pairs = []
    for table in diff_tables:
        # Iterate over each row in tbody
        for row in table.find_all("tr"):
            # Iterate over each cell in the row
            cells = row.find_all("td")
            if len(cells) < 4:
                continue

            data_marker0 = cells[0].get("data-marker")
            data_marker2 = cells[2].get("data-marker")

            if data_marker0 == '-' or data_marker2 == '+':
                original = cells[1].get_text()
                after = cells[3].get_text()
                # print(">>==================")
                # print(original)
                # print("====================")
                # print(after)
                # print("==================<<\n")
                original_html = str(cells[1].prettify())
                after_html = str(cells[3].prettify())
                # print("\n>>==================")
                # print(original_html)
                # print("====================")
                # print(after_html)
                # print("==================<<\n")
                pairs.append({
                    'before': original,
                    'after': after,
                    'before_source':original_html,
                    'after_source':after_html
                })
    return pairs


def process_data(filepath, outpath):
    print("reading data...")
    df = read_csv(filepath)
    revisions = []
    dataset = read_data(df)
    print("extracting pairs...")
    for i in tqdm(range(len(dataset))):
        data = dataset[i]
        labels = data['labels']
        if len(labels) != 1: # only keep pairs with one category
            continue

        rev_id = data['rev_id']
        url = f"https://en.wikipedia.org/wiki/WP:Labels?diff={rev_id}"

        pairs = get_wikipedia_revision(url)
        for pair in pairs:
            pair['label'] = labels[0]
            revisions.append(copy.copy(pair))

    print("store dataset...")
    store_csv(revisions, outpath)
    print("Done!")

if __name__ == '__main__':
    filepath = "./edit_intention_dataset.csv"
    outpath = "./edit_intention_dataset_processed.csv"
    process_data(filepath, outpath)
    # df = read_csv(filepath)
    # read_data(df)

    # url = "https://en.wikipedia.org/wiki/WP:Labels?diff=712140761"
    # revision_changes = get_wikipedia_revision(url)

    # for change in revision_changes:
    #     print(change)