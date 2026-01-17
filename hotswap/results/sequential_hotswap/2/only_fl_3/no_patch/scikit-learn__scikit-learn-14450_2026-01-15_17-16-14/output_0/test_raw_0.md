```python
import numpy as np
import sklearn.cross_decomposition

def main():
    try:
        reproduce_issue()
        print("Issue not present")
    except AssertionError as e:
        print("Issue reproduced successfully")
        print_stacktrace(e)
        raise e  # To make it clear an error occurred, though the script should still exit with an error due to unhandled exception

def reproduce_issue():
    pls2 = sklearn.cross_decomposition.PLSRegression()
    xx = np.random.random((5,5))
    yy = np.zeros((5,5))

    yy[0,:] = [0,1,0,0,0]
    yy[1,:] = [0,0,0,1,0]
    yy[2,:] = [0,0,0,0,1]
    #yy[3,:] = [1,0,0,0,0] # Uncommenting this line solves the issue

    try:
        pls2.fit(xx, yy)
    except ValueError as e:
        if "array must not contain nan" in str(e).lower():
            raise AssertionError("Issue present: PLS reports 'array must not contain nan' if a feature is constant") from e

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

if __name__ == "__main__":
    main()
```