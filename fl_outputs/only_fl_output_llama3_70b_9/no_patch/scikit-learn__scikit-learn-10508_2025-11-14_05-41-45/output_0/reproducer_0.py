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
    le.fit([1,2])
    assert np.array_equal(le.transform([]), np.array([], dtype=np.int64))

    le = LabelEncoder()
    le.fit(["a","b"])
    try:
        le.transform([])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("LabelEncoder transform fails for empty lists")

if __name__ == "__main__":
    main()
