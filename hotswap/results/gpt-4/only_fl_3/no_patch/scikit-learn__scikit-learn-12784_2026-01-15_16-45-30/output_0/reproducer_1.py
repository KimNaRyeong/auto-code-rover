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

def reproduce_kneighborsregressor_issue():
    import numpy as np
    import pandas as pd
    from sklearn.datasets import load_boston
    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsRegressor

    dataset = load_boston()
    target = dataset.target
    data = pd.DataFrame(dataset.data, columns=dataset.feature_names)

    np.random.seed(42)
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2)

    try:
        predict_sums = []
        for n_jobs in [1, 3, -1]:
            model = KNeighborsRegressor(n_jobs=n_jobs, algorithm='brute', metric='seuclidean')
            model.fit(X_train, y_train)
            predict_sum = np.sum(model.predict(X_test))
            predict_sums.append(predict_sum)
            print(f"Sum of predictions with n_jobs={n_jobs}: {predict_sum}")

        assert all(predict_sum == predict_sums[0] for predict_sum in predict_sums), \
            "KNeighborsRegressor gives different results for different n_jobs values"

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with a non-zero code to indicate failure

if __name__ == "__main__":
    reproduce_kneighborsregressor_issue()
