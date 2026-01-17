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

def reproduce_bug():
    import numpy as np
    from sklearn.mixture import GaussianMixture
    
    X = np.random.rand(1000, 10)
    for random_state in range(100):
        try:
            gm1 = GaussianMixture(n_components=2, n_init=1, random_state=random_state).fit(X)
            gm2 = GaussianMixture(n_components=2, n_init=10, random_state=random_state).fit(X)
            assert gm2.lower_bound_ > gm1.lower_bound_, random_state
        except AssertionError as e:
            print_stacktrace(e)
            exit(1)  # Exit with error when the issue presents

if __name__ == "__main__":
    reproduce_bug()
    print("No issue detected.")
```

This script defines a function `reproduce_bug` which tries to reproduce the issue described. It fits two Gaussian Mixture models with `n_components=2` on a random dataset of size `(1000, 10)` for `100` different `random_state` values. The first model is fit with `n_init=1`, and the second one with `n_init=10`. It asserts that the `lower_bound_` of the model fitted with `n_init=10` is always greater than the one fitted with `n_init=1`, as expected due to the increased number of initializations providing a better convergence on average.

When this assertion fails, it captures the `AssertionError`, prints a detailed stack trace using the `print_stacktrace` function, and exits with a status code of `1` to indicate the presence of the issue. If the loop completes without any assertions failing, it prints "No issue detected." indicating the bug is likely fixed or not present in the version of scikit-learn being used.