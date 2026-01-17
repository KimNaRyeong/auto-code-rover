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

def main():
    import numpy as np
    from sklearn.mixture import GaussianMixture

    X = np.random.rand(1000, 10)
    failed_states = []
    for random_state in range(100):
        try:
            # Fit with n_init=1
            gm1 = GaussianMixture(n_components=2, n_init=1, random_state=random_state).fit(X)
            # Fit with n_init > 1
            gm2 = GaussianMixture(n_components=2, n_init=10, random_state=random_state).fit(X)
            # Check if gm2's lower_bound_ is indeed higher (or equal, considering float inaccuracies)
            assert gm2.lower_bound_ >= gm1.lower_bound_, f"Failed for random_state={random_state}"
        except AssertionError as e:
            failed_states.append(random_state)
            print_stacktrace(e)

    if not failed_states:
        print("Issue not reproduced. All checks passed.")
    else:
        print(f"Issue reproduced for random_state(s): {', '.join(map(str, failed_states))}")

if __name__ == "__main__":
    main()
```

This code attempts to reproduce the described issue in a standalone script format. The script checks whether `GaussianMixture`'s `lower_bound_` with `n_init=10` is indeed not consistently higher than or equal to the lower bound when `n_init=1` across 100 different random states. When the assertion fails for at least one random state, an `AssertionError` will be thrown, and the stack trace of the error will be printed clearly showing the specific random state for which the test failed. The script exits with code 0 (successful exit status) if no issues are detected, printing a confirmation message. Otherwise, it documents the random states that reproduce the issue.