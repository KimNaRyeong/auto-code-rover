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

def reproduce_issue():
    import numpy as np
    from sklearn.mixture import GaussianMixture

    X = np.random.rand(1000, 10)
    for random_state in range(100):
        try:
            gm1 = GaussianMixture(n_components=2, n_init=1, random_state=random_state).fit(X)
            gm2 = GaussianMixture(n_components=2, n_init=10, random_state=random_state).fit(X)
            assert gm2.lower_bound_ >= gm1.lower_bound_, random_state
        except AssertionError as e:
            print_stacktrace(e)
            break
    else:  # This part runs if the loop completes without breaking (i.e., no error)
        print("No issue detected.")

if __name__ == "__main__":
    reproduce_issue()
```

This script is designed to run at the root directory of your project as specified and will check for the described bug by timing the lower bounds of `GaussianMixture` with `n_init` set to 1 against `n_init` set to 10 for `100` random states. When the condition fails, it will print a detailed stack trace of the issue using the provided `print_stacktrace` function. If the script does not encounter any assertion errors, it'll print `"No issue detected."` suggesting that the issue might be fixed or not present.