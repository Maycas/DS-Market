from sklearn import model_selection


def train_test_val_split(X, y, train_pct, test_pct, seed=42):
    """
    Given a set of features 'X' and a set of outcomes 'y', it generates the 3 
    datasets needed to train, test and validate a model.

    The function also accepts a 'train_pct' and a 'test_pct' to be able to define the 
    percentages of rows included in each one of the train, test and validation datasets.
    For the validation dataset it uses the remaining percentage
    """

    # splitting into train + test + validation
    # in the first split, we will split the data into training and the remaining data set. We are getting 80% of all samples
    X_train, X_rem, y_train, y_rem = model_selection.train_test_split(
        X,
        y,
        train_size=train_pct,
        random_state=seed
    )

    # since we now want to have the test and validation sizes to be equal, we will divide the sizes of X_rem by 50%
    X_val, X_test, y_val, y_test = model_selection.train_test_split(
        X_rem,
        y_rem,
        test_size=test_pct / (1 - train_pct),
        random_state=seed
    )
    return X_train, X_test, X_val, y_train, y_test, y_val
