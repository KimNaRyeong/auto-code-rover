import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    test = TfidfVectorizer(dtype=np.float32)
    result = test.fit_transform(["Help I have a bug"])
    expected_dtype = np.float32
    actual_dtype = result.dtype
    assert expected_dtype == actual_dtype, f"Expected dtype {expected_dtype} but got {actual_dtype}"
    print("Issue not reproduced. The output dtype matches the specified dtype.")
