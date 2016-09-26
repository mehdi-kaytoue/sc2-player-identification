import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
import sys
from sklearn import metrics
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn import tree


df = pd.read_csv("replay-features.txt")
train_data = df.values
target = train_data[:, -1:].ravel()
features = train_data[:, :-2]
for i in range(0, len(target)):
    if "WhiteRa" not in target[i]:
        target[i] = "0"
    else:
        target[i] = "1"
print("Data read.")

X_train, X_test, y_train, y_test = cross_validation.train_test_split(features,target, test_size=0.5, random_state=0)
model = RandomForestClassifier(max_features=None)
model.fit(X_train, y_train)
predicted = model.predict(X_test)

fpr, tpr, thresholds = metrics.roc_curve([int(a) for a in y_test], [int(a) for a in predicted], pos_label=1)
print("auc", metrics.auc(fpr, tpr))
print("accuracy", metrics.accuracy_score(y_test, predicted))
