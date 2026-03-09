# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

NUM_POS = 87
NUM_NEG = 130
pos_labels = [1] * NUM_POS
neg_labels = [-1] * NUM_NEG
pos_labels.extend(neg_labels)

def load_image(path: str) -> np.ndarray:
    temp = [[0 for _ in range(30)] for _ in range(20)]
    with open(path) as infile:
        rf = infile.readlines()
    for i in range(min(len(rf), 20)):
        for j in range(min(len(rf[i]), 30)):
            if rf[i][j] == '#':
                temp[i][j] = 1
    return np.array(temp).reshape(600)

pos_features = [load_image(f"data/train8/{k}.txt") for k in range(1, NUM_POS + 1)]
neg_features = [load_image(f"data/trainOthers/{k}.txt") for k in range(1, NUM_NEG + 1)]

features = pd.concat([
    pd.DataFrame(pos_features),
    pd.DataFrame(neg_features),
], ignore_index=True)

features["LABEL"] = pos_labels
features = features.iloc[np.random.permutation(len(features))]
features.to_csv("features.csv", index=False)
print("features.csv written.")
