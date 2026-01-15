```python
# reproducer.py
import numpy as np
from sklearn.mixture import GaussianMixture

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
    X = np.random.rand(1000, 10)
    for random_state in range(100):
        try:
            gm1 = GaussianMixture(n_components=2, n_init=1, random_state=random_state).fit(X)
            gm2 = GaussianMixture(n_components=2, n_init=10, random_state=random_state).fit(X)
            assert gm2.lower_bound_ > gm1.lower_bound_, random_state
        except AssertionError as e:
            print_stacktrace(e)
            raise SystemExit(1) # Exit with error code to indicate failure in reproducing issue

if __name__ == "__main__":
    main()
    print("No issues detected.") # This line is only reached if no AssertionError occurred
```

This script attempts to reproduce the described issue by fitting Gaussian Mixture Models with `n_init=1` and `n_init=10` and checks if the `lower_bound_` of the model initialized more times is indeed higher as expected. In case of an AssertionError, it prints the stacktrace of the error including the line numbers where it occurred, making it easier to identify and debug the issue. If no error occurs, it prints a message indicating no issues were detected.