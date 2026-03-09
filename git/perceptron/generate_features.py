# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd


def load_image(path: str) -> np.ndarray:
    temp = [[0 for _ in range(30)] for _ in range(20)]
    with open(path) as infile:
        rf = infile.readlines()
    for i in range(min(len(rf), 20)):
        for j in range(min(len(rf[i]), 30)):
            if rf[i][j] == '#':
                temp[i][j] = 1
    return np.array(temp).reshape(600)


def load_dir(directory: str) -> tuple[list[np.ndarray], int]:
    files = sorted(
        [f for f in os.listdir(directory) if f.endswith(".txt")],
        key=lambda f: int(f.replace(".txt", ""))
    )
    return [load_image(os.path.join(directory, f)) for f in files], len(files)


pos_features, NUM_POS = load_dir("data/train8")
neg_features, NUM_NEG = load_dir("data/trainOthers")

pos_labels = [1] * NUM_POS
neg_labels = [-1] * NUM_NEG
pos_labels.extend(neg_labels)

features = pd.concat([
    pd.DataFrame(pos_features),
    pd.DataFrame(neg_features),
], ignore_index=True)

features["LABEL"] = pos_labels
features = features.iloc[np.random.permutation(len(features))]
features.to_csv("features.csv", index=False)
print("features.csv written.")
