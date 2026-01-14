Below is a corrected Python script tailored to your requirements. This script checks the behavior of `LabelEncoder` with both integer and string inputs when transforming empty lists. It's designed to raise an `AssertionError` if the issue is present, which means it fails to transform an empty list after fitting with strings but not with integers. On the contrary, if the issue is resolved (empty lists can be transformed regardless of previous inputs without errors), it will exit quietly with code 0. The specified error printing function is included to detail any exceptions caught during execution.

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

def test_labelencoder_empty_transform():
    from sklearn.preprocessing import LabelEncoder
    import numpy as np
    
    le = LabelEncoder()

    # Case 1: Fit with integer labels
    le.fit([1, 2])
    try:
        assert np.array_equal(le.transform([]), np.array([], dtype=int)), "Empty list transform failed post integer fit."
    except Exception as e:
        print_stacktrace(e)
        print("Case 1 failed.")
        raise AssertionError("Failed to transform an empty list after fitting with integers.")

    # Case 2: Fit with string labels
    le.fit(["a", "b"])
    try:
        # This is where we expect the issue, based on reported behavior.
        assert np.array_equal(le.transform([]), np.array([], dtype='<U32')), "Empty list transform failed post string fit."
        print("No issue encountered. Exiting with code 0.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Failed to transform an empty list after fitting with strings.")

if __name__ == "__main__":
    test_labelencoder_empty_transform()
```

Make sure you're using the environment where the issue was observed: Python 3.6.3 and scikit-learn 0.19.1. Execution of this script should precisely demonstrate whether the underlying issue with transforming empty lists in `LabelEncoder` is still present or not, based on the specification provided.