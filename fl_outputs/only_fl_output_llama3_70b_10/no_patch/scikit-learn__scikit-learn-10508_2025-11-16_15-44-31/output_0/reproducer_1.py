import numpy as np
from sklearn.preprocessing import LabelEncoder

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
    le = LabelEncoder()
    le.fit(["a","b"])
    try:
        result = le.transform([])
        assert np.array_equal(result, np.array([], dtype=object)), "Empty array not returned for string labels"
    except TypeError as e:
        print_stacktrace(e)
        raise AssertionError("Expected empty array for string labels")

if __name__ == "__main__":
    main()
