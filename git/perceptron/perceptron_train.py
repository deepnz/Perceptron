# -*- coding: utf-8 -*-

import pandas as pd

num_features = 600
WEIGHTS: list[float] = [0.0] * 602
LEARNING_RATE = 0.10
MAX_ITERATIONS = 15
BIAS = 0.10


def find_sum(x_vec, weights: list[float]) -> float:
    ans = weights[0]
    for i in range(len(x_vec)):
        ans += x_vec[i] * weights[i + 1]
    return ans


def update_weight(x_vec, weights: list[float], error: float, learning_rate: float) -> list[float]:
    for i in range(len(weights) - 1):
        weights[i + 1] = weights[i + 1] + learning_rate * x_vec[i] * error
    return weights


WEIGHTS[0] = BIAS
training_features = pd.read_csv("features.csv")
labels = training_features.LABEL.tolist()
del training_features["LABEL"]

epoch = 0
while epoch < MAX_ITERATIONS:
    print(f"epoch: {epoch}")
    num_mis = 0
    for i in range(len(training_features)):
        x_vec = training_features.iloc[i]
        label = labels[i]
        output = 1 if find_sum(x_vec, WEIGHTS) > 0 else -1
        error = label - output
        if error != 0:
            num_mis += 1
        WEIGHTS = update_weight(x_vec, WEIGHTS, error, LEARNING_RATE)
    print(f"misclassifications: {num_mis}")
    epoch += 1

pd.DataFrame(WEIGHTS).to_csv("weights.csv", index=False)
print("weights.csv written.")
