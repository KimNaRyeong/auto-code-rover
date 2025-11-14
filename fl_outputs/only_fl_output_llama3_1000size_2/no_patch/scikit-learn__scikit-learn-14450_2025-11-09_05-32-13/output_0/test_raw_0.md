Here is the reproducer script:

```py
import numpy as np
import sklearn.cross_decomposition
from sklearn.exceptions import NotFittedError

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
    pls2 = sklearn.cross_decomposition.PLSRegression()
    xx = np.random.random((5,5))
    yy = np.zeros((5,5) ) 

    yy[0,:] = [0,1,0,0,0]
    yy[1,:) = [0,0,0,1,0]
    yy[2,:] = [0,0,0,0,1]
    #yy[3,:] = [1,0,0,0,0]  # Uncommenting this line solves the issue

    pls2.fit(xx, yy)
except NotFittedError as e:
    print_stacktrace(e)
    raise AssertionError("Issue reproduced")
```

This script will reproduce the issue by attempting to fit a PLSRegression model with an array that contains all zeros in one of its columns. If the issue is present (i.e., the `NotFittedError` is raised), it will print the stack trace and then raise an `AssertionError`.