You can use the following `reproducer.py` script. It attempts to fit an `MLPRegressor` with a very high number of iterations specified and checks if the actual number of iterations matches the expected. If the issue is present, it will raise an `AssertionError` and print a stack trace.

```python
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

def main():
    import numpy as np
    from sklearn.neural_network import MLPRegressor

    # Simulate a simple dataset
    X = np.arange(-5, 5, 0.1).reshape(-1, 1)
    y = X ** 2 # A simple non-linear relationship

    max_iter = 18000
    clf = MLPRegressor(max_iter=max_iter, activation='relu', solver='lbfgs', verbose=False)

    try:
        clf.fit(X, y)
        # We expect n_iter_ to be > 15000 given max_iter=18000, if the issue is present n_iter_ will be <= 15000
        assert clf.n_iter_ > 15000, f"Training did not run for more than 15000 iterations, stopped at {clf.n_iter_}. Issue with max_iter not properly applied."
        print("The issue is resolved.")
    except AssertionError as ae:
        print_stacktrace(ae)
        raise SystemExit(1) from ae

if __name__ == "__main__":
    main()
```

This script includes the necessary function for printing a precise stack trace if an exception occurs. It fits an `MLPRegressor` with a specified `max_iter` far beyond the default limitation of 15000 iterations. If the number of iterations (`n_iter_`) does not exceed 15000, it is indicative of the issue being present. If the script executes without exceptions, it implies the issue might have been resolved in your environment.