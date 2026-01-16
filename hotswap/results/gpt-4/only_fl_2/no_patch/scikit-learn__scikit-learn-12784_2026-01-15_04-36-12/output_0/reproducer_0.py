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
    # Import required packages
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

    # Function to create and test a model with different n_jobs
    def test_model(n_jobs):
        model = KNeighborsRegressor(n_jobs=n_jobs, algorithm='brute', metric='seuclidean')
        model.fit(X_train, y_train)
        return np.sum(model.predict(X_test))

    # Compare predictions
    sum_n_jobs_1 = test_model(1)
    sum_n_jobs_3 = test_model(3)
    sum_n_jobs_all = test_model(-1)

    # Raise an AssertionError if results are inconsistent
    assert np.isclose(sum_n_jobs_1, sum_n_jobs_3, rtol=1e-4), "n_jobs=1 and n_jobs=3 results differ"
    assert np.isclose(sum_n_jobs_1, sum_n_jobs_all, rtol=1e-4), "n_jobs=1 and n_jobs=-1 results differ"

except AssertionError as e:
    print_stacktrace(e)
    raise e

print("No discrepancy found. Exiting with code 0.")
