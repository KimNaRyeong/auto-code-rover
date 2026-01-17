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
