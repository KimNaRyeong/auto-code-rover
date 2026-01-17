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
