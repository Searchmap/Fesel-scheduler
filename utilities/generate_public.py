import numpy as np
import pickle

import pandas as pd 

from time import sleep

schema = {
    'sex': ['M', 'F'],
    'age': ['child', 'young', 'young_adult', 'adult', 'middle_aged', 'senior'],
    'skn': ['arab', 'asian','black', 'indian', 'white'],
}

def make_item(schema):
    return dict(
        [
            (key, np.random.choice(val, replace=True, size=1).tolist())
            for key, val in schema.items()
        ]
    )

def merge_item(items):
    dtfs = [ pd.DataFrame.from_dict(item) for item in items ]
    merged = pd.concat(dtfs, ignore_index=True)
    return merged

if __name__ == '__main__':
    print('[ ... Builder ... ]')
    G = []
    nb_frames = 1000
    for _ in range(nb_frames):
        acc = []
        nb_persons = np.random.randint(1, 20)
        for idx in range(nb_persons):
            item = make_item(schema)
            acc.append(item)

        
        merged = merge_item(acc)
        print(merged)
        
        G.append(merged)
    
    pickle.dump(G, open('source/database.pkl', 'wb'))