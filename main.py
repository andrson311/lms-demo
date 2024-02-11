import os
import pandas as pd
from tqdm import tqdm
from difflib import SequenceMatcher
from kaggle.api.kaggle_api_extended import KaggleApi

ROOT = os.path.dirname(__file__)

def get_data():
    api = KaggleApi()
    api.authenticate()

    api.dataset_download_file(
        'cclark/product-item-data',
        file_name='sample-data.csv',
        path=ROOT
    )

    df = pd.read_csv(os.path.join(ROOT, 'sample-data.csv'))

    return df

def find_near_duplicates(df, target):
    output = pd.DataFrame(columns=['id', 'LMS', 'identical'])

    for _, row in tqdm(df.iterrows()):

        text = row['description']

        s = SequenceMatcher(None, text, target, autojunk=False)
        result = s.find_longest_match(0, len(text), 0, len(target))

        product = {
            'id': row['id'],
            'LMS': result[2],
            'identical': (result[2] / int(len(text))) * 100
        }

        output = pd.concat([output, pd.DataFrame([product])], ignore_index=True)
    
    return output.sort_values(by='LMS', ascending=False)

if __name__ == '__main__':
    
    data = get_data()
    data = data[:30]

    for _, row in data.iterrows():
        desc = row['description']
        result = find_near_duplicates(data, desc)
        print(result.head())
    

