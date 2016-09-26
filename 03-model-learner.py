import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
from sklearn import metrics
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn import tree
from collections import Counter
import time, argparse


global args # Program arguments, global variable


def encode_target(df, target_column):
    """Add column to df with integers for the target.
    Args
    ----
    df -- pandas DataFrame.
    target_column -- column to map to int, producing
                     new Target column.
    Returns
    -------
    df_mod -- modified DataFrame.
    targets -- list of target names.
    """
    df_mod = df.copy()
    targets = df_mod[target_column].unique()
    map_to_int = {name: n for n, name in enumerate(targets)}
    df_mod[target_column] = df_mod[target_column].replace(map_to_int)
    return(df_mod, targets)


def remove_unpopulated_classes(_df, target_column, threshold):
    """
    Removes any row of the df for which the label in target_column appears less
    than threshold times in the whole frame (not enough populated classes)
    :param df: The dataframe to filter
    :param target_column: The target column with labels
    :param threshold: the number of appearances a label must respect
    :return: The filtered dataframe
    """
    count = Counter(_df[target_column])
    valid = [k for k in count.keys() if count[k] >= threshold]
    _df = _df[_df[target_column].isin(valid)]
    return _df


def main():
    global args
    df = pd.read_csv("replay-features.txt")
    df2, _ = encode_target(df, "battleneturl")
    df3, _ = encode_target(df2, "race")
    df4 = remove_unpopulated_classes(df3, "battleneturl", 20)
    train_data = df4.values
    target = train_data[:, -1:].ravel()
    features = train_data[:, :-1]
    print("Data read.")

    # Cross validation
    model = RandomForestClassifier(max_features=None)
    print(model.get_params())
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(features,target, test_size=0.2, random_state=0)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(score)

    # 5 Cross validation
    model = RandomForestClassifier(max_features=None)
    print(model.get_params())
    scores = cross_validation.cross_val_score(model, features, target, cv=5, scoring='accuracy')
    print("accuracy: ", scores)
    scores = cross_validation.cross_val_score(model, features, target, cv=5, scoring='precision_micro')
    print("precision:", scores)


if __name__ == '__main__':
    global args
    start_time = time.time()
    #parser = argparse.ArgumentParser(description="""@TODO""")  # @TODO Give a clear description of the script.
    #parser.add_argument('IN', type=str, help="INPUT")
    #parser.add_argument('OUT', type=str, help="OUTPUT")
    #args = parser.parse_args()
    main()
    print("--- Finished in " + str(int(time.time() - start_time)) + " seconds ---")
