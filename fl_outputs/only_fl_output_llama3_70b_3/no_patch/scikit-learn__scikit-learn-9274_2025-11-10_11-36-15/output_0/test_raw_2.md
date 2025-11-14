Here is a new standalone python file `reproducer.py` to reproduce the issue:
```
from __future__ import print_function
import numpy as np
from sklearn.neural_network import MLPRegressor

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
    # Load the data
    train = np.load("data.npy").tolist()

    max_iter = 18000
    clf = MLPRegressor(max_iter=max_iter, activation='relu', solver='lbfgs', verbose=True)
    clf.fit(train["train_x"], train["train_y"])
    print("score: ", clf.score(train["train_x"], train["train_y"]))
    print("iters: ", clf.n_iter_, " / ", max_iter)

    assert clf.n_iter_ == max_iter, f"Expected {max_iter} iterations, but got {clf.n_iter_}"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script assumes that the `data.npy` file is in the same directory. You can download the `data.npy` file from the provided gist link.

Please make sure to install scikit-learn correctly and have the `data.npy` file in the same directory before running this script.