import numpy as np
import pandas as pd
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor

# Prepare the dataset
dataset = load_boston()
target = dataset.target
data = pd.DataFrame(dataset.data, columns=dataset.feature_names)

# Split the dataset
np.random.seed(42)
X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2)

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    # Create a regressor with seuclidean distance and passing V as additional argument
    model_n_jobs_1 = KNeighborsRegressor(n_jobs=1, algorithm='brute', metric='seuclidean')
    model_n_jobs_1.fit(X_train, y_train)
    prediction_1 = np.sum(model_n_jobs_1.predict(X_test))

    # Create a regressor with seuclidean distance and passing V as additional argument
    model_n_jobs_3 = KNeighborsRegressor(n_jobs=3, algorithm='brute', metric='seuclidean')
    model_n_jobs_3.fit(X_train, y_train)
    prediction_3 = np.sum(model_n_jobs_3.predict(X_test))

    # Create a regressor with seuclidean distance and passing V as additional argument
    model_n_jobs_all = KNeighborsRegressor(n_jobs=-1, algorithm='brute', metric='seuclidean')
    model_n_jobs_all.fit(X_train, y_train)
    prediction_all = np.sum(model_n_jobs_all.predict(X_test))

    assert np.allclose([prediction_1, prediction_3, prediction_all], [prediction_1]*3), "Predictions are not equal"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
