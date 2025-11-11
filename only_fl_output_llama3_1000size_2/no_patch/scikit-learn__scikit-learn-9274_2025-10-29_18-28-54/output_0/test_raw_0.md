Here is the reproducer script:

```python
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

def reproduce_issue():
    try:
        train = np.load("data.npy").tolist()
        max_iter = 18000
        clf = MLPRegressor(max_iter=max_iter, activation='relu', solver='lbfgs', verbose=True)
        clf.fit(train["train_x"], train["train_y"])
        print("score: ", clf.score(train["train_x"], train["train_y"]))
        print("iters: ", clf.n_iter_, " / ", max_iter)
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script will load the data, create an MLP regressor with `max_iter` set to 18000 and solver set to 'lbfgs', fit the model, and then try to score the model. If any exception occurs during this process, it will print the stack trace and raise the exception again.