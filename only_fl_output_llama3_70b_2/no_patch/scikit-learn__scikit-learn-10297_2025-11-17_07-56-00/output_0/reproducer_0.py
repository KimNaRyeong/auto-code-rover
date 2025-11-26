import numpy as np
from sklearn import linear_model as lm

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

try:
    # test database
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.normal(size=n)

    rr = lm.RidgeClassifierCV(alphas=np.arange(0.1, 1000, 0.1), normalize=True, 
                              store_cv_values=True).fit(x, y)

    assert False, "Expected TypeError: __init__() got an unexpected keyword argument 'store_cv_values'"
except TypeError as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
