```python
# reproducer.py

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

def test_gaussian_mixture_lower_bound():
    import numpy as np
    from sklearn.mixture import GaussianMixture

    X = np.random.rand(1000, 10)
    for random_state in range(100):
        gm1 = GaussianMixture(n_components=2, n_init=1, random_state=random_state).fit(X)
        gm2 = GaussianMixture(n_components=2, n_init=10, random_state=random_state).fit(X)
        try:
            assert gm2.lower_bound_ >= gm1.lower_bound_, f"Failed for random_state={random_state}"
        except AssertionError as e:
            print_stacktrace(e)
            exit(1)  # Exit with error code to indicate failure

    print("Test passed: lower_bound_ is correctly reported.")
    exit(0)  # Exit code 0 to indicate success

if __name__ == "__main__":
    test_gaussian_mixture_lower_bound()
```

This script is designed to reproduce the described issue with the `GaussianMixture` class in the scikit-learn library, where when `n_init` is greater than 1, the `lower_bound_` property should reflect the maximum lower bound across all initializations but allegedly does not. It runs a test to ensure that the `lower_bound_` of a `GaussianMixture` model with `n_init=10` is always greater than or equal to the `lower_bound_` of a model with `n_init=1`, using a variety of random states.

- If the test fails for any random state, the script prints a detailed stack trace for the assert statement that failed, showing the random state that caused the failure, and exits with error code 1.
- If all tests pass and no issues are found, the script prints a success message and exits with code 0, indicating successful execution.

Please, run `python3 reproducer.py` within the project's root directory to execute the test and observe the behavior. If the issue described in the original problem statement is present, the script will exit with an error code and print a stack trace for the first failed assertion. If the issue has been fixed, the script will exit with code 0, indicating that the test passed successfully.