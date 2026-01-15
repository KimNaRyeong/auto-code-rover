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

def test_KNeighborsRegressor_n_jobs_issue():
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
    
    try:
        outcomes = []
        for n_jobs in [1, 3, -1]:
            # Create and fit the regressor
            model = KNeighborsRegressor(n_jobs=n_jobs, algorithm='brute', metric='seuclidean')
            model.fit(X_train, y_train)

            # Make predictions and sum them up to compare
            predictions_sum = np.sum(model.predict(X_test))
            outcomes.append(predictions_sum)

        # Check if the outcomes are the same for different n_jobs values
        assert np.std(outcomes) < 1e-5, "Outcomes should be nearly identical!"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("KNeighborsRegressor gives different results for different n_jobs values.")

if __name__ == "__main__":
    test_KNeighborsRegressor_n_jobs_issue()
